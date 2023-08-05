import modelingDash.configModelisation as cm
import modelingDash.explorePumpTrialsDash as pumpTabs
from dorianUtils.dccExtendedD import DccExtended
import dash, dash_core_components as dcc, dash_html_components as html, dash_bootstrap_components as dbc

folderData = '/home/dorian/data/sylfenData/essaisPumps/'

dccE = DccExtended()
app  =  dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],title='pumpTrials',url_base_pathname = '/pumpTrials/')

pumpTrialsTab  = pumpTabs.ExplorePumpTrialsDash(app,folderData)
compareTab  = pumpTabs.ComparePumpTrialsDash(app,folderData)

titleHTML=html.H1('explore trials of pumps V1.1')
tabsLayout = html.Div(dccE.createTabs([pumpTrialsTab,compareTab]))
# tabsLayout = html.Div(dccE.createTabs([pumpTrialsTab]))
app.layout = html.Div([html.Div(titleHTML),html.Div(tabsLayout)])

app.run_server(port=65000,debug=True,use_reloader=False)
# app.run_server(port=65000,host='0.0.0.0',debug=False)
