import importlib
import dash, dash_core_components as dcc, dash_html_components as html, dash_bootstrap_components as dbc
import dorianUtils.dccExtendedD as dcce
import dorianUtils.configFilesD as cfd
import screeningBuilding.screeningBuildingTabs as sbtbabs

# ==============================================================================
#                       INSTANCIATIONS
# ==============================================================================
baseFolder = '/home/dorian/data/sylfenData/'
folderPkl  = baseFolder + 'monitoring_pkl/'
pklMeteo  = baseFolder + 'meteo_pkl/'

dccE=dcce.DccExtended()

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],title='small power explorer',url_base_pathname = '/smallPowerDash/')
folderPkl  = baseFolder + 'monitoring_pkl/'
pklMeteo  = baseFolder + 'meteo_pkl/'

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],title='cool',url_base_pathname = '/test/')
# tabMultiUnits = sbtbabs.MultiUnitSmallPowerTab(folderPkl,app)
tabSelectedTags = sbtbabs.TagSelectedScreeningBuilding(folderPkl,app,pklMeteo=pklMeteo)
computationTab = sbtbabs.ComputationTab(app,folderPkl)
# tabUnitSelector = sbtbabs.TabUnitSelector(folderPkl,app),

titleHTML=html.H1('Screening Building V3.2')
# tabsLayout= dccE.createTabs([tabSelectedTags,tabUnitSelector,tabMultiUnits,tabModule,tabCompute])
tabsLayout= dccE.createTabs([tabSelectedTags,computationTab])
app.layout = html.Div([html.Div(titleHTML),html.Div(tabsLayout)])
app.run_server(port=45001,debug=True,use_reloader=False)
