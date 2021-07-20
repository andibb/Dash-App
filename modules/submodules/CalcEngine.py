import numpy as np

class CalcEngine():

    def __init__(self,pd,relativedelta):
        self.pd = pd
        self.relativedelta = relativedelta
        print("CalcEngine initiated")

    def calc_statistical(self,metada_grp_call):
        #calculation of statistical forecast
        for region in metada_grp_call:
            df_historical = metada_grp_call[region]['historical']
            df_historical = df_historical.groupby(df_historical.index.hour).mean()

            # get forecast for: wind, solar  generation from EntsoE

            df_wind_and_solar = metada_grp_call[region]['forecast']['entsoe_wind_and_solar']
            df_wind_and_solar = df_wind_and_solar.groupby(df_wind_and_solar.index.hour).mean()

            #df_wind_and_solar['Wind and Solar'] = df_wind_and_solar.sum(axis=1)  <-- weiss nicht wofür ich das gemacht hatte :-)

            # alle gemittelten daten der letzten wochen, bis auf die Vorhersage für wind und solar
            df_forecast = df_historical

            # überschreibe die Vorhersage durch Wind & Vorhersage von EntsoE 
            try:
                df_forecast["Wind Onshore"] = df_wind_and_solar["Wind Onshore"]
                df_forecast["Wind Offshore"] = df_wind_and_solar["Wind Offshore"]
                df_forecast["Solar"] = df_wind_and_solar["Solar"]
            except KeyError:
                print("No Wind Offshore")

            start = metada_grp_call[region]['forecast']['entsoe_wind_and_solar'].index[0]
            df_forecast.index = df_forecast.index.map(lambda x: start + self.relativedelta(hours = x))
        return(df_forecast)

    def calc_gC02(self,df):
        #funktion um gC02/kWh (intensität) des Stroms zu errechnen, hierzu brauchte ich die Daten für den jeweiligen energie-konstituenten
        # Quelle: https://www.wegatech.de/ratgeber/photovoltaik/grundlagen/co2-bilanz-photovoltaik/
        # PV: 50, Braunkohle 1075, Steinkohle 830, Erdgas 500, Wasserkraft 23, Windkraft 18
        # alle Angaben sind in gC02/KWh 
        gc02_per_kWh = {'Biomass':50,'Fossil Brown coal/Lignite':1075,'Fossil Gas':500,'Fossil Hard coal':830,'Fossil Oil':900,'Geothermal':0,'Hydro Water Reservoir':23,'Hydro Pumped Storage':23,'Hydro Run-of-river and poundage':23,'Nuclear':10,'Other':500,'Other renewable':100,'Solar':50,'Waste':50,'Wind Onshore':18,'Wind Offshore':18}
        for el in df:
            df[el] = df[el]*gc02_per_kWh[el]
        df = df.sum(axis=1)
        return df

    def calc_percentage(self,df):
        #funktion um prozent der erneuerbaren energieträger zu errechnen
        #Der Funktion werden ein pd.Dataframe und eine liste an Energieträgern übergeben
        #als return erhält man den prozentualen Anteil der übergebenen Energieträger.
        #input: pd.Dataframe, list
        #output: pd.Dataframe
        #calculates the percentage of renewable energy of the produced energy mix
        renewable_energies= ["Biomass","Geothermal","Hydro Pumped Storage","Hydro Run-of-river and poundage","Other renewable","Solar","Wind Onshore","Wind Offshore"]
        try:
            df = round(df.loc[:,df.columns.intersection(renewable_energies)].sum(axis=1)/df.sum(axis=1),3)
            return df*100
        except KeyError as e:
            try :
                renewable_energies.remove(e.args[0][2:15]) 
                df = df.loc[:,lambda df: renewable_energies].sum(axis=1)//df.sum(axis=1)
                return df*100
            except ValueError:
                print("Bitte wählen Sie einen gültigen Energieträger")
                return 0
    