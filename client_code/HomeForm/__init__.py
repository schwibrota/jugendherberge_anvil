from ._anvil_designer import HomeFormTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from datetime import date


class HomeForm(HomeFormTemplate):
  def __init__(self, **properties):
   
    self.init_components(**properties)
    self.date_picker_1.min_date = date.today()
    self.date_picker_1.date = date.today()
    self.date_picker_2.min_date = date.today()

    
    print(anvil.server.call('get_gaeste'))
    self.drop_down_1.items = anvil.server.call('get_jugendherbergen', "name, JID")
    self.drop_down_2.items = anvil.server.call('get_gaeste')
    print(self.drop_down_1.items[self.drop_down_1.selected_value-1])
    

    self.drop_down_1_change()


    

  
  def drop_down_1_change(self, **event_args):
    jid = self.drop_down_1.items[self.drop_down_1.selected_value - 1][1]
    items = anvil.server.call('get_zimmer', jid, "zimmernummer, bettenanzahl, preis_pro_nacht")

    toAdd = []
    for item in items:
      temp = {'zimmernummer':item[0], 'personen':item[1], 'preis':item[2]}
      toAdd.append(temp)
    self.repeating_panel_1.items = toAdd

    pass

  def drop_down_2_change(self, **event_args):
    print(anvil.server.call('get_ungebuchte_zimmer'))
    self.drop_down_3.items = anvil.server.call('get_ungebuchte_zimmer')
    pass

  def date_picker_1_change(self, **event_args):
    self.date_picker_2.min_date = self.date_picker_1.date
    pass

  def button_1_click(self, **event_args):
    if self.date_picker_1.date:
      if self.date_picker_2.date:
        open_form('Form1', self.date_picker_1.date, self.date_picker_2.date, self.drop_down_3.items[self.drop_down_3.selected_value][1])
    pass