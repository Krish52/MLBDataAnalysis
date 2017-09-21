import pandas as pd
import pymysql
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
import kivy.uix.checkbox
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from itertools import chain

global player_info, player_stats, player_cmp, player_id

#----------Main APP class----------
class MlbDataApp(App):
    def build(self):
        # Set the background color for the window
        Window.clearcolor = (.3, .3, .3, .3)

#----------Class for Main Box Layout and Home Page----------
class MlbDataAnalysis(BoxLayout):
    # ----------Get Player firstname and lastname----------
    def mlb_data(self):
        global player_info, player_stats, compare_players, input_ln, input_fn
        input_fn = str(self.firstname_input.text)
        input_ln = str(self.lastname_input.text)
        #print(input_fn, input_ln)                              ----> for debugging

        # ----------Checking the Radio Button Selection----------
        if player_info == True:
            # ----------if Player Info is selected----------
            conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='root', db='lahman2016')
            cur = conn.cursor()
            # ----------Getting the player information from Database using Pymysql to connect to mysql----------
            cur.execute("SELECT birthYear, birthMonth, birthDay, birthCountry, Height, Weight, Throws, Debut FROM Master "
                        "WHERE nameFirst = '{}' AND nameLast = '{}'".format(input_fn, input_ln))
            result = cur.fetchone()
            # ----------Displaying the Data on a popup window----------
            text = Label(text="Player Name : {} {}\nBirth Date : {}-{}-{}\nBirth Country : {}\nDebut : {}\n"
                              "Height(inches) : {}\nWeight(lbs) : {}\nThrow Hand : {}\n"
                         .format(input_fn,input_ln, result[0], result[1], result[2], result[3], result[7],
                                 result[4], result[5], result[6]))
            popup = Popup(title='Player Information', content=text, size_hint=(None, None), size=(400, 400))
            popup.open()

        elif player_stats == True:
            # ----------elif Player Stats is selected----------
            conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='root', db='lahman2016')
            cur = conn.cursor()
            # ----------Getting the player ID from Database and forwarding it to StatsPopup class----------
            cur.execute("SELECT playerID FROM Master WHERE nameFirst = '{}' AND nameLast = '{}'"
                        .format(input_fn, input_ln))
            result = cur.fetchall()
            MlbDataAnalysis.player_id = str(list(chain(*result)))
            popup = StatsPopup()
            popup.open()

        elif player_cmp == True:
            # ----------elif Compare Players is selected----------
            conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='root', db='lahman2016')
            cur = conn.cursor()
            # ----------Getting the player ID from Database and forwarding it to ComparePopup class----------
            cur.execute("SELECT playerID FROM Master WHERE nameFirst = '{}' AND nameLast = '{}'"
                        .format(input_fn, input_ln))
            result = cur.fetchall()
            MlbDataAnalysis.player_id = str(list(chain(*result)))
            popup = ComparePopup()
            popup.open()

    def cb_player_info(self): #Setting player_info to True
        global player_info, player_stats, player_cmp
        player_info = True
        player_stats = False
        player_cmp = False
        #print("Player info Set to true")                           ----> for debugging
        #print(player_info, player_stats, player_cmp)               ----> for debugging

    def cb_player_stats(self): #Setting player_stats to True
        global player_info, player_stats, player_cmp
        player_info = False
        player_stats = True
        player_cmp = False
        #print("Player Stats set to true")                          ----> for debugging
        #print(player_info, player_stats, player_cmp)               ----> for debugging

    def cb_player_cmp(self): #Setting player_cmp to True (cmp - Compare)
        global player_info, player_stats, player_cmp
        player_info = False
        player_stats = False
        player_cmp = True
        #print("Player Compare set to true")                        ----> for debugging
        #print(player_info, player_stats, player_cmp)               ----> for debugging

    def clear_home(self):#Clearing text boxes when Clear is pressed
        self.firstname_input.text = ""
        self.lastname_input.text = ""

#----------Class to display the player Stats----------
class StatsPopup(Popup):
    #----------__init__----------
    def __init__(self, **kwargs):
        self.pick_category()
        super(StatsPopup, self).__init__(**kwargs)

    # ----------Values for Category Spinner----------
    def pick_category(self):
        self.choose_category = ['Batting', 'Pitching', 'Fielding']
        self.year_list = ['Year']

    # ----------Method to get the yearlist for the spinner, using the Player ID----------
    def popup_yearlist(self, category_text):
        player_id = MlbDataAnalysis.player_id.strip("['']")
        conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='root', db='lahman2016')
        cur = conn.cursor()
        # ----------Gets the year list from Batting Table----------
        if category_text == 'Batting':
            #print("He is a hitter")                                ----> for debugging
            cur.execute("SELECT batting.yearID FROM batting "
                        "INNER JOIN master ON batting.playerID = master.playerID WHERE master.playerID = '{}'".format(player_id))
            result = cur.fetchall()
            year = list(chain(*result))
            cur.execute("SELECT batting.stint FROM batting "
                        "INNER JOIN master ON batting.playerID = master.playerID WHERE master.playerID = '{}'".format(player_id))
            result = cur.fetchall()
            stint = list(chain(*result))
            self.year_list = []
            self.stint_list = []
            #print(year, stint)                                     ----> for debugging
            for i in range(0, len(year)):
                self.year_list.append(str(year[i]) + ' - ' + str(stint[i]))
            # ----------Set the Spinner Values----------
            self.ids.spinner_stats_year.values = self.year_list
        # ----------Gets the year list from Pitching Table----------
        elif category_text == 'Pitching':
            #print("He is a pitcher")                               ----> for debugging
            cur.execute("SELECT pitching.yearID FROM pitching "
                        "INNER JOIN master ON pitching.playerID = master.playerID WHERE master.playerID = '{}'".format(
                player_id))
            result = cur.fetchall()
            year = list(chain(*result))
            cur.execute("SELECT pitching.stint FROM pitching "
                        "INNER JOIN master ON pitching.playerID = master.playerID WHERE master.playerID = '{}'".format(
                player_id))
            result = cur.fetchall()
            stint = list(chain(*result))
            self.year_list = []
            self.stint_list = []
            #print(year, stint)                                     ----> for debugging
            for i in range(0, len(year)):
                self.year_list.append(str(year[i]) + ' - ' + str(stint[i]))
            self.ids.spinner_stats_year.values = self.year_list

        # ----------Gets the year list from Fielding Table----------
        elif category_text == 'Fielding':
            #print("He is a Fielder")                               ----> for debugging
            cur.execute("SELECT fielding.yearID FROM fielding "
                        "INNER JOIN master ON fielding.playerID = master.playerID WHERE master.playerID = '{}'".format(
                player_id))
            result = cur.fetchall()
            year = list(chain(*result))
            cur.execute("SELECT fielding.stint FROM fielding "
                        "INNER JOIN master ON fielding.playerID = master.playerID WHERE master.playerID = '{}'".format(
                player_id))
            result = cur.fetchall()
            stint = list(chain(*result))
            self.year_list = []
            self.stint_list = []
            #print(year, stint)                                     ----> for debugging
            for i in range(0, len(year)):
                self.year_list.append(str(year[i]) + ' - ' + str(stint[i]))
            self.ids.spinner_stats_year.values = self.year_list

    # ----------After selecting the Year and pressing GO----------
    def stats_popup_on_go(self):
        player_id = MlbDataAnalysis.player_id.strip("['']")
        var1, var2 = (self.ids.spinner_stats_year.text).split('-')
        conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='root', db='lahman2016')
        cur = conn.cursor()
        # ----------Gets the Batting Stats from Batting Table----------
        if self.ids.spinner_category.text == 'Batting':
            #print("Getting data from Batting Table")               ----> for debugging
            cur.execute("SELECT G, AB, R, H, 2B, 3B, HR, RBI, SB, CS, BB, SO FROM Batting WHERE "
                        "playerID = '{}' AND yearID = '{}' AND stint = '{}'".format(player_id, var1, var2))
            result = cur.fetchone()
            # ----------Displays the results on a popup----------
            text = Label(text="Stats : \nG : {}\nAB : {}\nR : {}\nH : {}\n2B : {}\n3B : {}\nHR : {}\nRBI : {}\n"
                              "SB : {}\nCS : {}\nBB : {}\nSO : {}\n"
                         .format(result[0], result[1], result[2], result[3],result[4], result[5], result[6], result[7],
                                 result[8], result[9], result[10], result[11]))
            popup = Popup(title='Batting Stats', content=text, size_hint=(None, None), size=(400, 400))
            popup.open()
        # ----------Gets the Pitching Stats from Pitching Table----------
        elif self.ids.spinner_category.text == 'Pitching':
            print("Getting data from Pitching Table")
            cur.execute("SELECT W, L, G, GS, CG, SHO, SV, IPouts, H, ER, HR, BB, ERA, SO, BK, R FROM Pitching WHERE "
                        "playerID = '{}' AND yearID = '{}' AND stint = '{}'".format(player_id, var1, var2))
            result = cur.fetchone()
            # ----------Display results on a Popup----------
            text = Label(text="Stats : \nW : {}\nL : {}\nG : {}\nGS : {}\nCG : {}\nSHO : {}\nSV : {}\nIPO : {}\n"
                              "H : {}\nER : {}\nHR : {}\nBB : {}\nERA : {}\nSO : {}\nBK : {}\nR : {}"
                         .format(result[0], result[1], result[2], result[3], result[4], result[5], result[6],
                                 result[7], result[8], result[9], result[10], result[11],result[12], result[13],
                                 result[14], result[15]))
            popup = Popup(title='Pitching Stats', content=text, size_hint=(None, None), size=(400, 600))
            popup.open()
        # ----------Gets the Fielding Stats from Fielding Table----------
        elif self.ids.spinner_category.text == 'Fielding':
            print("Getting data from Fielding Table")
            cur.execute("SELECT G, GS, INNOuts, PO, A, E, DP, PB FROM Fielding WHERE "
                        "playerID = '{}' AND yearID = '{}' AND stint = '{}'".format(player_id, var1, var2))
            result = cur.fetchone()
            # ----------Display results on a popup----------
            text = Label(text="Stats : \nG : {}\nGS : {}\nIO : {}\nPO : {}\nA : {}\nE : {}\nDP : {}\nPB : {}"
                         .format(result[0], result[1], result[2], result[3], result[4],
                                 result[5], result[6], result[7]))
            popup = Popup(title='Fielding Stats', content=text, size_hint=(None, None), size=(400, 400))
            popup.open()

# ----------Class to get Compare Stats from 2 players----------
class ComparePopup(Popup):
    global player2_id
    def __init__(self, **kwargs):
        self.pick_category()
        super(ComparePopup, self).__init__(**kwargs)

    def pick_category(self):
        self.choose_cmp_category = ['Batting', 'Pitching', 'Fielding']
        self.year_list = ['Year']

    def player2_name_enter(self, category_text):
        global player2_id
        player1_id = MlbDataAnalysis.player_id.strip("['']")
        conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='root', db='lahman2016')
        cur = conn.cursor()
        player2_fn = str(self.player2_input_fn.text)
        player2_ln = str(self.player2_input_ln.text)
        print(player2_fn, player2_ln)
        cur.execute("SELECT playerID FROM Master WHERE nameFirst = '{}' AND nameLast = '{}'"
                    .format(player2_fn, player2_ln))
        result = cur.fetchall()
        player2_id = str(list(chain(*result))).strip("['']")
        print(player1_id,player2_id)

        if category_text == 'Batting':
            #print("They are hitters")
            cur.execute("SELECT batting.yearID FROM batting "
                        "INNER JOIN master ON batting.playerID = master.playerID WHERE master.playerID = '{}'".format(
                player1_id))
            result = cur.fetchall()
            year_p1 = list(chain(*result))
            cur.execute("SELECT batting.stint FROM batting "
                        "INNER JOIN master ON batting.playerID = master.playerID WHERE master.playerID = '{}'".format(
                player1_id))
            result = cur.fetchall()
            stint_p1 = list(chain(*result))
            cur.execute("SELECT batting.yearID FROM batting "
                        "INNER JOIN master ON batting.playerID = master.playerID WHERE master.playerID = '{}'".format(
                player2_id))
            result = cur.fetchall()
            year_p2 = list(chain(*result))
            cur.execute("SELECT batting.stint FROM batting "
                        "INNER JOIN master ON batting.playerID = master.playerID WHERE master.playerID = '{}'".format(
                player2_id))
            result = cur.fetchall()
            stint_p2 = list(chain(*result))
            self.year_list_player1 = []
            self.stint_list_player1 = []
            self.year_list_player2 = []
            self.stint_list_player2 = []
            print(year_p1, stint_p1, year_p2, stint_p2)
            for i in range(0, len(year_p1)):
                self.year_list_player1.append(str(year_p1[i]) + ' - ' + str(stint_p1[i]))
            for i in range(0, len(year_p2)):
                self.year_list_player2.append(str(year_p2[i]) + ' - ' + str(stint_p2[i]))
            self.ids.spinner_cmp_p1_year.values = self.year_list_player1
            self.ids.spinner_cmp_p2_year.values = self.year_list_player2


        elif category_text == 'Pitching':
            #print("They are pitchers")
            cur.execute("SELECT pitching.yearID FROM pitching "
                        "INNER JOIN master ON pitching.playerID = master.playerID WHERE master.playerID = '{}'".format(
                player1_id))
            result = cur.fetchall()
            year_p1 = list(chain(*result))
            cur.execute("SELECT pitching.stint FROM pitching "
                        "INNER JOIN master ON pitching.playerID = master.playerID WHERE master.playerID = '{}'".format(
                player1_id))
            result = cur.fetchall()
            stint_p1 = list(chain(*result))
            cur.execute("SELECT pitching.yearID FROM pitching "
                        "INNER JOIN master ON pitching.playerID = master.playerID WHERE master.playerID = '{}'".format(
                player2_id))
            result = cur.fetchall()
            year_p2 = list(chain(*result))
            cur.execute("SELECT pitching.stint FROM pitching "
                        "INNER JOIN master ON pitching.playerID = master.playerID WHERE master.playerID = '{}'".format(
                player2_id))
            result = cur.fetchall()
            stint_p2 = list(chain(*result))
            self.year_list_player1 = []
            self.stint_list_player1 = []
            self.year_list_player2 = []
            self.stint_list_player2 = []
            print(year_p1, stint_p1, year_p2, stint_p2)
            for i in range(0, len(year_p1)):
                self.year_list_player1.append(str(year_p1[i]) + ' - ' + str(stint_p1[i]))
            for i in range(0, len(year_p2)):
                self.year_list_player2.append(str(year_p2[i]) + ' - ' + str(stint_p2[i]))
            self.ids.spinner_cmp_p1_year.values = self.year_list_player1
            self.ids.spinner_cmp_p2_year.values = self.year_list_player2

        elif category_text == 'Fielding':
            #print("They are Fielders")
            cur.execute("SELECT fielding.yearID FROM fielding "
                        "INNER JOIN master ON fielding.playerID = master.playerID WHERE master.playerID = '{}'".format(
                player1_id))
            result = cur.fetchall()
            year_p1 = list(chain(*result))
            cur.execute("SELECT fielding.stint FROM fielding "
                        "INNER JOIN master ON fielding.playerID = master.playerID WHERE master.playerID = '{}'".format(
                player1_id))
            result = cur.fetchall()
            stint_p1 = list(chain(*result))
            cur.execute("SELECT fielding.yearID FROM fielding "
                        "INNER JOIN master ON fielding.playerID = master.playerID WHERE master.playerID = '{}'".format(
                player2_id))
            result = cur.fetchall()
            year_p2 = list(chain(*result))
            cur.execute("SELECT fielding.stint FROM fielding "
                        "INNER JOIN master ON fielding.playerID = master.playerID WHERE master.playerID = '{}'".format(
                player2_id))
            result = cur.fetchall()
            stint_p2 = list(chain(*result))
            self.year_list_player1 = []
            self.stint_list_player1 = []
            self.year_list_player2 = []
            self.stint_list_player2 = []
            print(year_p1, stint_p1, year_p2, stint_p2)
            for i in range(0, len(year_p1)):
                self.year_list_player1.append(str(year_p1[i]) + ' - ' + str(stint_p1[i]))
            for i in range(0, len(year_p2)):
                self.year_list_player2.append(str(year_p2[i]) + ' - ' + str(stint_p2[i]))
            self.ids.spinner_cmp_p1_year.values = self.year_list_player1
            self.ids.spinner_cmp_p2_year.values = self.year_list_player2

    def cmp_popup_on_go(self):
        global player2_id
        player1_id = MlbDataAnalysis.player_id.strip("['']")
        var1, var2 = (self.ids.spinner_cmp_p1_year.text).split('-')
        var3, var4 = (self.ids.spinner_cmp_p2_year.text).split('-')
        #print(player2_id, player1_id)
        conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='root', db='lahman2016')
        cur = conn.cursor()
        if self.ids.spinner_cmp_category.text == 'Batting':
            #print("Getting data from Batting Table")
            cur.execute("SELECT G, AB, R, H, 2B, 3B, HR, RBI, SB, CS, BB, SO FROM Batting WHERE "
                        "playerID = '{}' AND yearID = '{}' AND stint = '{}'".format(player1_id, var1, var2))
            result_player1 = cur.fetchone()

            cur.execute("SELECT G, AB, R, H, 2B, 3B, HR, RBI, SB, CS, BB, SO FROM Batting WHERE "
                        "playerID = '{}' AND yearID = '{}' AND stint = '{}'".format(player2_id, var3, var4))
            result_player2 = cur.fetchone()
            text = Label(text="Title : Player 1 - Player 2\n"
                              "G : {} - {}\n"
                              "AB : {} - {}\n"
                              "R : {} - {}\n"
                              "H : {} - {}\n"
                              "2B : {} - {}\n"
                              "3B : {} - {}\n"
                              "HR : {} - {}\n"
                              "RBI : {} - {}\n"
                              "SB : {} - {}\n"
                              "CS : {} - {}\n"
                              "BB : {} - {}\n"
                              "SO : {} - {}\n"
                         .format(result_player1[0], result_player2[0], result_player1[1], result_player2[1],
                                 result_player1[2], result_player2[2], result_player1[3], result_player2[3],
                                 result_player1[4], result_player2[4], result_player1[5], result_player2[5],
                                 result_player1[6], result_player2[6], result_player1[7], result_player2[7],
                                 result_player1[8], result_player2[8], result_player1[9], result_player2[9],
                                 result_player1[10], result_player2[10], result_player1[11], result_player2[11],)
                         )
            popup = Popup(title='Comparing Batting Stats', content=text, size_hint=(None, None), size=(400, 400))
            popup.open()



        elif self.ids.spinner_cmp_category.text == 'Pitching':
            #print("Getting data from Pitching Table")
            cur.execute("SELECT W, L, G, GS, CG, SHO, SV, IPouts, H, ER, HR, BB, ERA, SO, BK, R FROM Pitching WHERE "
                        "playerID = '{}' AND yearID = '{}' AND stint = '{}'".format(player1_id, var1, var2))
            result_player1 = cur.fetchone()

            cur.execute("SELECT W, L, G, GS, CG, SHO, SV, IPouts, H, ER, HR, BB, ERA, SO, BK, R FROM Pitching WHERE "
                        "playerID = '{}' AND yearID = '{}' AND stint = '{}'".format(player2_id, var3, var4))
            result_player2 = cur.fetchone()
            text = Label(text="Title : Player 1 - Player 2\n"
                              "W : {} - {}\n"
                              "L : {} - {}\n"
                              "G : {} - {}\n"
                              "GS : {} - {}\n"
                              "CG : {} - {}\n"
                              "SHO : {} - {}\n"
                              "SV : {} - {}\n"
                              "IPO : {} - {}\n"
                              "H : {} - {}\n"
                              "ER : {} - {}\n"
                              "HR : {} - {}\n"
                              "BB : {} - {}\n"
                              "ERA : {} - {}\n"
                              "SO : {} - {}\n"
                              "BK : {} - {}\n"
                              "R : {} - {}\n"
                         .format(result_player1[0], result_player2[0], result_player1[1], result_player2[1],
                                 result_player1[2], result_player2[2], result_player1[3], result_player2[3],
                                 result_player1[4], result_player2[4], result_player1[5], result_player2[5],
                                 result_player1[6], result_player2[6], result_player1[7], result_player2[7],
                                 result_player1[8], result_player2[8], result_player1[9], result_player2[9],
                                 result_player1[10], result_player2[10], result_player1[11], result_player2[11],
                                 result_player1[12], result_player2[12], result_player1[13], result_player2[13],
                                 result_player1[14], result_player2[14], result_player1[15], result_player2[15])
                         )
            popup = Popup(title='Comparing Pitching Stats', content=text, size_hint=(None, None), size=(400, 600))
            popup.open()


        elif self.ids.spinner_cmp_category.text == 'Fielding':
            #print("Getting data from Fielding Table")
            cur.execute("SELECT G, GS, INNOuts, PO, A, E, DP, PB FROM Fielding WHERE "
                        "playerID = '{}' AND yearID = '{}' AND stint = '{}'".format(player1_id, var1, var2))
            result_player1 = cur.fetchone()

            cur.execute("SELECT G, GS, INNOuts, PO, A, E, DP, PB FROM Fielding WHERE "
                        "playerID = '{}' AND yearID = '{}' AND stint = '{}'".format(player2_id, var3, var4))
            result_player2 = cur.fetchone()
            text = Label(text = "Title : Player 1 - Player 2\n"
                                "G : {} - {}\n"
                                "GS : {} - {}\n"
                                "INNOuts : {} - {}\n"
                                "PO : {} - {}\n"
                                "A : {} - {}\n"
                                "E : {} - {}\n"
                                "DP : {} - {}\n"
                                "PB : {} - {}\n"
                         .format(result_player1[0],result_player2[0],result_player1[1],result_player2[1],
                                 result_player1[2], result_player2[2],result_player1[3],result_player2[3],
                                 result_player1[4], result_player2[4],result_player1[5],result_player2[5],
                                 result_player1[6], result_player2[6],result_player1[7],result_player2[7])
                         )
            popup = Popup(title='Comparing Fielding Stats', content=text,size_hint=(None, None), size=(400, 400))
            popup.open()

    def cmp_clear(self):
        self.player2_input_fn.text = ""
        self.player2_input_ln.text = ""


if __name__ == "__main__":
    MlbDataApp().run()