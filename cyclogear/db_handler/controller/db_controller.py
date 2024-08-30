from ast import literal_eval
from functools import partial

from ..model.db_handler import DbHandler
from ..view.Window import Window

class ViewSelectItemController:
    def __init__(self, model: DbHandler, view: Window, available_tables, limits):
        self._db_handler = model
        self._window = view
        self._available_tables = available_tables
        self._limits = limits

        self.selected_item_attributes = None
        self._init_ui()
        self._connect_signals_and_slots()

    def _init_ui(self):
        # Set active table
        self._active_table = self._available_tables[0]
        # Init view
        self._window.viewActiveTableSelector(self._available_tables)
        self._window.viewTableItems(self._db_handler.get_filtered_results(self._active_table, self._limits))
        self._window.viewFunctionButtons()

    def _connect_signals_and_slots(self):
        self._window.tableItemsView.itemsTable.itemClicked.connect(self._select_item_event)
        self._window.activeTableSelector.currentIndexChanged.connect(self._switch_active_table_event)
        self._window.okBtn.clicked.connect(partial(self._close_window_event, True))
        self._window.cancelBtn.clicked.connect(partial(self._close_window_event, False))

    def _switch_active_table_event(self, selected_table_index):
        # Check if selected table is not active table
        selected_table = self._available_tables[selected_table_index]
        if self._active_table is not selected_table:
            # Set new active table
            self._active_table = selected_table
            # Update view
            updated_results = self._db_handler.get_filtered_results(self._active_table, self._limits)
            self._window.tableItemsView.updateItemsView(updated_results)

    def _select_item_event(self, item):
        # Get the selected item attributes
        item_code = self._window.tableItemsView.getItemCode(item)
        item_data = self._db_handler.get_single_item(self._active_table, item_code)
        self.selected_item_attributes = item_data
        # Enable the OK button
        self._window.okBtn.setEnabled(True)
    
    def _close_window_event(self, item_selected):
        if item_selected:
            self._window.accept()
        else:
            self._window.reject()
    
    def startup(self):
        result = self._window.exec()
        return result == self._window.DialogCode.Accepted

class ViewDbTablesController:
    def __init__(self, model: DbHandler, view: Window):
        self._db_handler = model
        self._window = view
        
        self._startup()
        self._connect_signals_and_slots()
    
    def _startup(self):
        # Set active table
        self._available_tables = self._db_handler.get_available_tables()
        self._active_table = self._available_tables[0]
        # Get limits
        self._limits = self._db_handler.get_table_items_filters(self._active_table)
        # Init view
        self._window.viewTablesTree(self._available_tables)
        self._window.viewFilters(self._db_handler.get_table_items_attributes(self._active_table))
        self._window.viewTableItems(self._db_handler.get_filtered_results(self._active_table, self._limits))
    
    def _connect_signals_and_slots(self):
        self._window.tablesTreeView.tableSelectedSignal.connect(self._switch_active_table_event)
        self._window.itemsFiltersView.filterResultsButton.clicked.connect(self._update_results_event)
    
    def _switch_active_table_event(self, selected_table):
        # Check if selected table is not active table
        if selected_table and self._active_table is not selected_table:
            # Set new active table
            self._active_table = selected_table
            # Update limits - get them from new active table
            self._limits = self._db_handler.get_table_items_filters(self._active_table)
            # Update view
            updated_results = self._db_handler.get_filtered_results(self._active_table, self._limits)
            updatedAttributes = self._db_handler.get_table_items_attributes(self._active_table)
            self._window.tableItemsView.updateItemsView(updated_results)
            self._window.itemsFiltersView.updateFiltersView(updatedAttributes)
            self._window.tablesTreeView.updateActiveTable(self._active_table)

    def _update_results_event(self):
        # Update limits - get them from user inputs
        for attribute, attribute_limits in self._limits.items():
            for limit in attribute_limits:
                text = self._window.itemsFiltersView.filtersLineEdits[attribute][limit].text()
                number = literal_eval(text) if text else 0
                attribute_limits[limit] = number
        # Update items view
        updated_results = self._db_handler.get_filtered_results(self._active_table, self._limits)
        self._window.tableItemsView.updateItemsView(updated_results)
