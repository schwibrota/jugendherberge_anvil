from ._anvil_designer import Form1Template
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class Form1(Form1Template):
  def __init__(self, startdatum, enddatum, zid, **properties):
    
    self.init_components(**properties)
    
    self.label_1.text = f"Startdatum: {startdatum}\nEnddatum: {enddatum}\nZimmer: {anvil.server.call('get_preis_from_zid', zid)[0][0]}\nPreis pro Nacht: {anvil.server.call('get_preis_from_zid', zid)[0][1]}"

  def button_1_click(self, **event_args):
    # hier eine Buchung erstellen und das ganze ins Home Menü zurück steuern
    pass
