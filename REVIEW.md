# Ревью кода — feature/graph-updated                          
## 1. `gui/views/main_window.py` — критично много runtime-верстки   
### 1.1 Замена `tableValues` на `QTableView` (строки 27–33)                
- **Проблема:** в `mainwindow.ui` стоит `QTableWidget`, а в `__init__` он удаляется и заменяется на `QTableView`.
- **Что делать:** просто положить `QTableView` в `.ui` изначально. Никакой `replaceWidget`/`deleteLater` не нужен.                                                                        
### 1.2 Настройки таблиц — stretch, alternatingRowColors, скрытие verticalHeader (строки 38–43)
- **Проблема:** всё это можно задать в Designer (или в `.ui` XML), а не в коде.
- **Что делать:**                                                             
- `alternatingRowColors="true"` — есть в property Designer.                                                                                       
- `verticalHeader.setVisible(False)` — галочка в Designer (`verticalHeaderVisible`).                                                              
- `setSectionResizeMode(QHeaderView.Stretch)` — можно выставить в Designer или оставить в коде, если stretch логически зависит от данных.                                                                         
### 1.3 Навигация по страницам — `_build_workspace_pages` (строки 89–172)  
- **Проблема:** это самый большой кусок кода, который должен быть в `.ui`:
- `QStackedWidget` с 5 страницами создаётся вручную.                                                                                              
- Кнопки навигации вырываются из `nav_layout`, потом обратно вкладываются в новый `QHBoxLayout`.                                                  
- `tableValues`, `plotGroup`, `instrumentsGroup` удаляются из `verticalLayoutRight`, потом добавляются внутрь страниц `QStackedWidget`. 
- `constantsTable` создаётся полностью в коде, хотя это обычная `QTableView`.   
- **Что делать:**           
- В `mainwindow.ui` сделать готовый `QStackedWidget` с 5 страницами (`QWidget`  `QVBoxLayout` на каждой).                                        
- На страницу «Переменные» положить `tableValues` (QTableView).                                                                                   
- На страницу «Константы» положить `constantsTable` (QTableView).               
- На страницу «Приборы» положить `instrumentsGroup`.                                 
- На страницу «Графики» положить `plotGroup`.   
- На страницу «Формулы» положить `formulas_hint`.                               
- Кнопки навигации уже есть в `.ui` — их просто `connect` к `setCurrentIndex` stacked widget.                                                     
- Всё удаление/вставка/создание layout’ов в коде уйдёт — останется только логика переключения страниц и подсветки кнопок.                                      
### 1.4 Стили навигационных кнопок `_setup_page_nav_styles` (строки 50–82)                     
- **Проблема:** raw `setStyleSheet` для 5 кнопок в Python.                   
- **Что делать:**                          
- Либо вынести stylesheet в отдельный `.qss` файл и применять к `MainWindow` целиком. 
- Либо задать `styleSheet` property кнопкам в Designer.        
- Лучше использовать `QButtonGroup`  `setExclusive(True)`  `setCheckable(True)` — тогда подсветка «active» кнопки делается через CSS псевдокласс                                                                                           ---                                                                                                                                                                
## 2. `gui/views/plots.py` — костыль `moveUiContents`  `setup_base_ui`
### 2.1 Перенос layout из временного виджета (строки 21–44, 61–68)       
- **Проблема:** каждый plot создаёт `Ui_PlotBase()` на временном `QWidget`, потом вручную переносит дочерние виджеты через `takeAt(0)` в `parent_u… 
- **Почему плохо:** это хрупкий хак. При любом изменении `plot_base.ui` можно сломать порядок виджетов. 
- **Что делать:**        
- В каждом `.ui`-файле графика (`scatter_plot.ui`, `line_plot.ui` и т.д.) **вместо** пустого `parent_ui` положить **готовый** `PlotWidget` (prom… 
- Тогда `Ui_PlotBase` вообще не нужен отдельно — всё будет в одном `.ui` на график.                                                               
- Если хочется переиспользовать «оси  заголовок» — сделать `PlotBase` отдельным **custom widget** (наследник `QWidget` с `Ui_PlotBase` внутри), и использовать его в каждом графике через Widget Promotion.
### 2.2 Заполнение combo-box’ов символами (ScatterPlot, строки 130–133)    
 - **Проблема:** `symbolCombo` наполняется в Python.                         
- **Что делать:** добавить items прямо в `.ui` (через property `items` в Designer), либо сделать через enum/delegate, если данные динамические. Но в данном случае это просто статический список символов, так что можно положить прямо в `.ui`.                                
 ---                                                                          
## 3. `gui/views/plot_manager.py` — лишнее создание обёрток   
### 3.1 `PlotTab` создаёт `QWidget`  `QVBoxLayout` вручную (строки 26–30)         
- **Проблема:** это можно было бы сделать в `.ui`, но тут допустимо, т.к. вкладки динамические.                                                     
- **Минор:** `setTabsClosable(True)` можно задать в `mainwindow.ui` у `plotTabs`.                                                                                                                                                      
 ---                                                                          
## 4. `gui/controllers/dialog_controller.py` — диалоги через `QInputDialog`
### 4.1 Последовательные QInputDialog для создания переменной / прибора / константы
- **Проблема:** UX ужасный — 3–4 отдельных системных диалога подряд. Если пользователь ошибётся на последнем шаге, начинать заново.                 
- **Что делать:**                                                         
- Сделать **кастомные `.ui`-диалоги** (`add_variable_dialog.ui`, `add_instrument_dialog.ui`, `add_constant_dialog.ui`) с полями `QLineEdit`, `QC…
- Вызвать `QDialog.exec()` — один диалог, один результат.                                                                                         
- Это ровно то, о чём говорил преподаватель: вместо императивного кода диалогов — декларативный UI.                                       
## 5. `mainwindow.ui` — структура не соответствует коду                  
### 5.1 `tableValues` — тип `QTableWidget`                                 
- Нужен `QTableView`, т.к. используется `QAbstractTableModel`.              
### 5.2 `formulas_hint` (`QLabel`) лежит в корне `verticalLayoutRight`      
- Если сделать `QStackedWidget` в `.ui`, эта заглушка должна быть на 5-й странице, а не болтаться снаружи.                                                                        
### 5.3 Отсутствует `QStackedWidget` для страниц  
- В `.ui` нет stacked widget — он собирается целиком в Python.                                                               
### 5.4 Лишний `QTableWidget` → `QTableView` адаптер в `gui/models/`               
- Если `tableValues` станет `QTableView` в `.ui`, код подмены в`main_window.py` полностью исчезнет. ---                                                                                  
## 6. `gui/models/value_table_model.py` — нетривиальное поведение удаления      
### 6.1 Удаление значения по пустой строке (строки  151–157)                       
- **Проблема:** если в ячейке «Значение» стереть текст и нажать Enter, строка **удаляется** из списка. Это неочевидно для пользователя.             
- **Что делать:** либо добавить отдельную кнопку «Удалить строку», либо хотя бы показать `QMessageBox` с подтверждением, либо задокументировать в   ---                                                                                                                                     
## 7. Мелкие замечания                                                            
Файл   Строки   Проблема  Решение                                                   
 ------ -------- ---------- ---------                                       
`gui/controllers/main_controller.py`   41–55   `_ensure_seed_data` — хардкод стартовых данных   Вынести в отдельный `seed.py` или сделать через … 
`gui/controllers/main_controller.py`   221–223   `_instrument_type_label` — чисто UI-метка   Перенести как `display_name`/`type_label` в `Instru… 
`gui/models/instrument_table_model.py`   20   Прямой доступ `self._experiment._instruments`   Использовать публичный `get_instruments()`, либо е… 
`src/experiment.py`   14–46   Singleton через `__new__`   Допустимо, но усложняет тестирование. Рассмотреть обычный класс  передачу в контроллер экземпляра.
`src/variable.py`   87–151   `write_csv`/`read_csv` — логика сериализации в доменной модели   Лучше оставить только в `serializers/`, модель не …                                                                         ---                            
## Итоговый чек-лист для правок (по приоритету)                                   
1. **[UI]** Переделать `mainwindow.ui`: добавить `QStackedWidget` со страницами, заменить `QTableWidget` на `QTableView`, убрать `formulas_hint` и… 
2. **[Code]** Удалить `_build_workspace_pages` из `main_window.py` — всё уже будет в `.ui`.                                                         
3. **[UI/Code]** Сделать кастомные `.ui`-диалоги для добавления переменной/прибора/константы вместо цепочки `QInputDialog`.                         
4. **[UI/Code]** Убрать `moveUiContents`/`setup_base_ui` из `plots.py` — либо слить `plot_base.ui` в каждый график, либо сделать Widget Promotion.  
5. **[Code]** Вынести стили кнопок в `.qss` или property в Designer.       
6. **[Refactor]** Убрать `write_csv`/`read_csv` из `Variable` → полностью переложить на `CSVHandler`.
7. **[UX]** Добавить явное удаление строки в `ValueTableModel` (кнопка/контекстное меню) вместо удаления по пустой строке.                                                                        ---                  
*Дата ревью:*2026-05-04*                                               