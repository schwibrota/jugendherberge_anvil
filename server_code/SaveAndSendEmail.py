import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.files
from anvil.files import data_files
import anvil.server
import sqlite3

# This is a server module. It runs on the Anvil server,
# rather than in the user's browser.
#
# To allow anvil.server.call() to call functions here, we mark
# them with @anvil.server.callable.
# Here is an example - you can replace it with your own:
#
@anvil.server.callable
def say_hello(name):
  print("Hello, " + name + "!")
  return 42

@anvil.server.callable
def get_jugendherbergen(rows="*"):
  conn = sqlite3.connect(data_files['jugendherbergen_verwaltung.db'])
  cursor = conn.cursor()
  res = list(cursor.execute(f"SELECT {rows} FROM jugendherbergen"))
  return res
  
@anvil.server.callable
def get_zimmer(jid,rows="*"):
  conn = sqlite3.connect(data_files['jugendherbergen_verwaltung.db'])
  cursor = conn.cursor()
  res = list(cursor.execute(f"SELECT {rows} FROM zimmer WHERE JID = {jid}"))
  conn.close()
  return res
  
@anvil.server.callable
def get_gaeste(rows="*"):
  conn = sqlite3.connect(data_files['jugendherbergen_verwaltung.db'])
  cursor = conn.cursor()
  res = list(cursor.execute(f"SELECT {rows} FROM gast"))
  conn.close()
  gesamt = []
  for i in range(len(res)):
    temp = (f"{res[i][1]} {res[i][2]}", res[i][0])
    gesamt.append(temp)
  return gesamt


@anvil.server.callable
def get_ungebuchte_zimmer():
  conn = sqlite3.connect(data_files['jugendherbergen_verwaltung.db'])
  cursor = conn.cursor()
  res = list(cursor.execute("SELECT ZID, zimmernummer FROM zimmer WHERE gebucht = 0"))
  conn.close()
  gesamt = []
  for i in range(len(res)):
    temp = (f'{res[i][1]}', res[i][0])
    gesamt.append(temp)
  return gesamt

@anvil.server.callable
def get_preis_from_zid(zid):
  conn = sqlite3.connect(data_files['jugendherbergen_verwaltung.db'])
  cursor = conn.cursor()
  res = list(cursor.execute(f"SELECT zimmernummer, preis_pro_nacht FROM zimmer WHERE ZID = {zid}"))
  conn.close()
  return res

@anvil.server.callable
def save_booking(startdate, enddate, gid, zid):
  conn = sqlite3.connect(data_files['jugendherbergen_verwaltung.db'])
  cursor = conn.cursor()
  cursor.execute(f"INSERT INTO buchung (startdatum, enddatum, gast_id, zid) VALUES ({startdate}, {enddate}, {gid}, {zid})")
  cursor.execute(f"UPDATE zimmer SET gebucht = 1 WHERE ZID = {zid}")
  # Immer wenn ich das Gebucht auf 1 Setze, wird es zwar übernommen, wenn ich es printe, doch wenn ich es in einer anderen Funktion abfrage,
  # wird es immer noch als 0 interpretiert...
  print(list(cursor.execute(f"SELECT * FROM zimmer WHERE ZID = {zid}")))
  conn.close()