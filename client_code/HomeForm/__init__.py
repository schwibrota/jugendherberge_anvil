from ._anvil_designer import HomeFormTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server


class HomeForm(HomeFormTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    
    print(anvil.server.call("say_hello", "sauron"))
    print(anvil.server.call("get_jugendherbergen"))
    self.drop_down_1.items = anvil.server.call('get_jugendherbergen', "name, JID")
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

  