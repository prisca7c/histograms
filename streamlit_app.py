import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
from io import StringIO

# ============================================================================
# CONFIGURATION SECTION
# ============================================================================

# Page configuration
st.set_page_config(
    page_title="Distribution Fitting Tool",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for aesthetic styling with ergonomic color scheme
st.markdown("""
    <style>
    /* Import Google Font - Noto Sans JP for Japanese style */
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@300;400;500;700&display=swap');
    
    /* Global font and background */
    * {
        font-family: 'Noto Sans JP', sans-serif;
    }
    
    /* Main background - dark for high contrast */
    .main {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        padding: 2rem;
        color: #f0f0f0;
    }
    
    /* Hide sidebar by default */
    [data-testid="stSidebar"] {
        display: none;
    }
    
    /* Center and style main title - Japanese minimalist */
    h1 {
        text-align: center;
        color: #ffffff;
        font-family: 'Noto Sans JP', sans-serif;
        font-weight: 300;
        font-size: 3rem;
        letter-spacing: 8px;
        margin-bottom: 0.5rem;
        text-transform: uppercase;
        border-bottom: 2px solid #e94560;
        padding-bottom: 1.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    /* Subtitle */
    .subtitle {
        text-align: center;
        color: #b0b0b0;
        font-size: 1.1rem;
        font-weight: 300;
        margin-bottom: 2rem;
        letter-spacing: 2px;
    }
    
    /* Section headers */
    h2 {
        color: #e94560;
        font-weight: 400;
        font-size: 1.6rem;
        margin-top: 2rem;
        margin-bottom: 1.5rem;
        border-left: 4px solid #e94560;
        padding-left: 1rem;
        letter-spacing: 2px;
    }
    
    h3 {
        color: #f0f0f0;
        font-weight: 500;
        font-size: 1.3rem;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
        letter-spacing: 1px;
    }
    
    /* All text elements */
    p, label, span, div {
        color: #e0e0e0;
    }
    
    /* Metric containers - dark theme */
    [data-testid="stMetric"] {
        background-color: #0f3460;
        padding: 1.2rem;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.4);
        border: 1px solid #5eaaa8;
        margin: 0.5rem 0;
    }
    
    [data-testid="stMetric"] label {
        color: #b0b0b0 !important;
    }
    
    [data-testid="stMetric"] [data-testid="stMetricValue"] {
        color: #ffffff !important;
    }
    
    /* Input areas */
    .stTextArea textarea {
        background-color: #0f3460;
        border: 2px solid #5eaaa8;
        border-radius: 6px;
        font-family: 'Noto Sans JP', monospace;
        color: #ffffff;
        padding: 0.8rem;
    }
    
    .stTextArea label {
        color: #f0f0f0 !important;
    }
    
    /* Radio buttons */
    .stRadio label {
        color: #f0f0f0 !important;
    }
    
    .stRadio > label {
        color: #f0f0f0 !important;
    }
    
    /* Selectbox */
    .stSelectbox label {
        color: #f0f0f0 !important;
    }
    
    /* File uploader */
    .stFileUploader label {
        color: #f0f0f0 !important;
    }
    
    /* Buttons */
    .stButton button {
        background-color: #e94560;
        color: white;
        border-radius: 6px;
        border: none;
        padding: 0.5rem 2rem;
        font-weight: 500;
        transition: all 0.3s ease;
        letter-spacing: 1px;
    }
    
    .stButton button:hover {
        background-color: #c7354f;
        box-shadow: 0 4px 16px rgba(233, 69, 96, 0.5);
    }
    
    /* Tables */
    table {
        font-family: 'Noto Sans JP', sans-serif;
        background-color: #0f3460;
        border-radius: 8px;
        overflow: hidden;
        color: #ffffff;
    }
    
    table thead tr th {
        background-color: #e94560 !important;
        color: #ffffff !important;
    }
    
    table tbody tr {
        background-color: #0f3460 !important;
    }
    
    table tbody tr td {
        color: #e0e0e0 !important;
    }
    
    /* Tabs - Japanese style */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
        background-color: transparent;
        border-bottom: 2px solid #e94560;
        margin-bottom: 2rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: transparent;
        border-radius: 8px 8px 0 0;
        padding: 1rem 2.5rem;
        font-weight: 400;
        color: #b0b0b0;
        border: none;
        letter-spacing: 2px;
        margin-bottom: -2px;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #0f3460;
        color: #e94560;
        border: 2px solid #5eaaa8;
        border-bottom: 2px solid #0f3460;
    }
    
    /* Info/Success/Warning boxes */
    .stAlert {
        font-family: 'Noto Sans JP', sans-serif;
        border-radius: 6px;
        border-left: 4px solid;
        background-color: #0f3460;
        color: #f0f0f0;
    }
    
    /* Markdown text */
    .stMarkdown {
        color: #e0e0e0;
    }
    
    /* Dataframe */
    .stDataFrame {
        background-color: #0f3460;
    }
    
    /* Slider styling */
    .stSlider {
        padding: 1rem 0;
    }
    
    .stSlider label {
        color: #f0f0f0 !important;
    }
    
    /* Slider track - rounded edges */
    .stSlider [data-baseweb="slider"] {
        background-color: #0f3460;
    }
    
    .stSlider [role="slider"] {
        border-radius: 50%;
    }
    
    /* Slider rail */
    .stSlider > div > div > div > div {
        border-radius: 8px;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background-color: #0f3460;
        border-radius: 6px;
        font-weight: 500;
        color: #f0f0f0;
    }
    
    /* Spinner */
    .stSpinner > div {
        border-top-color: #e94560 !important;
    }
    
    /* Horizontal rule */
    hr {
        border-color: #e94560;
    }
    </style>
""", unsafe_allow_html=True)

# Title and description
st.markdown('<div style="text-align: center; color: #ffffff; font-family: \'Roboto\', sans-serif; font-weight: 300; font-size: 2.8rem; letter-spacing: 2px; margin-bottom: 0.5rem; text-transform: uppercase; border-bottom: 3px solid #e94560; padding-bottom: 1.5rem;">STATISTICAL DISTRIBUTION FITTING TOOL</div>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Prisca Chien || 21178781 || 2 Dec 2025 || NE 111</p>', unsafe_allow_html=True)

# ============================================================================
# DISTRIBUTION DEFINITIONS (10+ Types Required)
# ============================================================================

DISTRIBUTIONS = {
    'Normal': {'dist': stats.norm, 'params': ['loc', 'scale']},
    'Gamma': {'dist': stats.gamma, 'params': ['a', 'loc', 'scale']},
    'Weibull': {'dist': stats.weibull_min, 'params': ['c', 'loc', 'scale']},
    'Exponential': {'dist': stats.expon, 'params': ['loc', 'scale']},
    'Lognormal': {'dist': stats.lognorm, 'params': ['s', 'loc', 'scale']},
    'Beta': {'dist': stats.beta, 'params': ['a', 'b', 'loc', 'scale']},
    'Chi-Square': {'dist': stats.chi2, 'params': ['df', 'loc', 'scale']},
    'Uniform': {'dist': stats.uniform, 'params': ['loc', 'scale']},
    'Logistic': {'dist': stats.logistic, 'params': ['loc', 'scale']},
    'Pareto': {'dist': stats.pareto, 'params': ['b', 'loc', 'scale']},
    'Rayleigh': {'dist': stats.rayleigh, 'params': ['loc', 'scale']},
    'Student-t': {'dist': stats.t, 'params': ['df', 'loc', 'scale']}
}

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def parse_data(data_input):
    """Parse comma or space-separated data"""
    try:
        # Replace commas with spaces and split
        data_str = data_input.replace(',', ' ')
        values = [float(x) for x in data_str.split() if x.strip()]
        return np.array(values)
    except:
        return None

def fit_distribution(data, dist_obj):
    """Fit distribution to data and return parameters using scipy.stats"""
    try:
        params = dist_obj.fit(data)
        return params
    except:
        return None

def calculate_fit_quality(data, dist_obj, params):
    """Calculate goodness of fit metrics: MSE, Max Error, KS test"""
    # Create histogram
    hist, bin_edges = np.histogram(data, bins='auto', density=True)
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
    
    # Get theoretical density
    theoretical = dist_obj.pdf(bin_centers, *params)
    
    # Calculate metrics
    mse = np.mean((hist - theoretical) ** 2)
    max_error = np.max(np.abs(hist - theoretical))
    
    # Calculate Kolmogorov-Smirnov statistic
    ks_stat, ks_pvalue = stats.kstest(data, lambda x: dist_obj.cdf(x, *params))
    
    return {
        'MSE': mse,
        'Max Error': max_error,
        'KS Statistic': ks_stat,
        'KS p-value': ks_pvalue
    }

def plot_distribution(data, dist_obj, params, dist_name, ax):
    """Plot histogram and fitted distribution visualization - matches example code structure"""
    # Set figure background
    ax.set_facecolor('#ffffff')
    
    # Create distribution object with fitted parameters (like example: dist = gamma(*params))
    dist = dist_obj(*params)
    
    # Create x range for fitted distribution (like example: x = np.linspace(0, 25, 100))
    x_min = max(0, data.min() - 1)
    x_max = data.max() + 1
    x = np.linspace(x_min, x_max, 100)
    
    # Get fitted distribution PDF (like example: fit = dist.pdf(x))
    fit = dist.pdf(x)
    
    # Plot fitted distribution line first (like example: ax.plot(x, fit))
    ax.plot(x, fit, color='#e94560', linewidth=2.5, label=f'Fitted {dist_name}')
    
    # Plot histogram second (like example: ax.hist(data, bins=25, density=True))
    ax.hist(data, bins=25, density=True, alpha=0.7, color='#5eaaa8', edgecolor='#2c5282', label='Data')
    
    ax.set_xlabel('Value', fontsize=12, fontfamily='sans-serif', color='#000000', labelpad=10)
    ax.set_ylabel('Density', fontsize=12, fontfamily='sans-serif', color='#000000', labelpad=10)
    ax.set_title(f'Data Distribution with Fitted {dist_name}', fontsize=14, fontweight='400', 
                 fontfamily='sans-serif', color='#2c3e50', pad=15)
    ax.legend(fontsize=11, framealpha=0.95, facecolor='#f8f9fa', edgecolor='#bdc3c7', 
              labelcolor='#2c3e50', loc='best')
    ax.grid(True, alpha=0.3, linestyle='--', color='#95a5a6')
    ax.tick_params(colors='#000000', labelsize=10, pad=5)
    
    # Set spine colors - neutral gray
    for spine in ax.spines.values():
        spine.set_edgecolor('#bdc3c7')
        spine.set_linewidth(1)

# ============================================================================
# DATA INPUT SECTION (Manual Entry + CSV Upload)
# ============================================================================

# Create two-column layout for data input and configuration
input_col, config_col = st.columns([1, 1])

with input_col:
    st.markdown("<p style='font-weight:500; font-size:1.6rem; color:#e94560; margin-top:1.5rem; margin-bottom:1.5rem; border-left:4px solid #e94560; padding-left:1rem; letter-spacing:2px;'>Data Input</p>", unsafe_allow_html=True)
    
    input_method = st.radio("Choose input method:", ["Manual Entry", "CSV Upload"])
    
    data = None
    
    # Manual data entry
    if input_method == "Manual Entry":
        st.markdown("**Enter data (comma or space-separated):**")
        data_input = st.text_area(
            "Data values:", 
            value="3.20719972771444,2.87129040067153,5.78729035553647,4.1187091291734,4.38892441143452,5.51983579411947,7.90659610041574,14.2464130461306,5.53262079779466,8.71231628950114,4.11483534889389,4.21676261414512,3.80742490832028,8.12295261344642,14.4931193240959,4.17061928235844,5.56473369646821,3.85601850903497,6.65482199070973,5.64527500798778,3.69470891623014,5.71475936880442,6.42321075793331,4.18764978676313,8.48363880632814,4.3185065867552,2.63868243051386,12.063722658557,4.53786350503291,4.01908595867652,3.67080036194595,10.0441547890996,5.7819839771617,1.53178808027106,5.98977516511071,10.9771080475445,3.47981915074114,3.17809729624012,5.76866572512802,2.65246319401473,3.1704720430555,7.26893066922843,4.10425656738533,12.0308139249766,21.8249355000441,6.44870668778663,3.63812351193026,6.87382124371665,15.2735394703434,7.38970347326533,2.69998527504317,10.4273336307952,6.11206256383201,4.5920968801287,8.65133221986743,2.62055704470486,6.99683810153907,2.98062919587173,4.44388439043336,5.7530123869902,11.1124482663633,7.78578215883215,4.45029285710677,1.9727820396507,5.99676189263169,3.05730606830652,4.19050957866747,4.3724444814354,9.25822133955263,4.84488764535786,5.67149615372399,5.3289426461222,9.0276128378506,5.00796339010461,5.10030909308932,4.69790795067666,7.52632897929432,4.9432432444583,11.5095934486767,6.68703481963587,5.36989828756535,2.29582109778393,4.53261357074735,1.3226152010431,6.46993019723354,6.48511130955385,3.67395379810723,1.61658582601082,5.17157558544848,3.43650525236362,2.56686623161152,10.703070445034,1.22466181525404,11.9659048285323,3.93698457790289,3.10356261351468,8.07916089821821,5.06656410453392,10.0288206488804,3.44832191263857,5.07295045294818,4.22728051634265,8.88562310807271,3.84281527048915,6.47788459861068,6.07548869902777,6.29919843406497,4.45789001647914,6.59424659355596,4.33996583353805,2.35516092352541,5.60138675446724,9.43844175490494,4.8860664222843,6.78064974445323,3.46240429257522,8.28805367606514,5.19882192072884,10.2912444101418,3.88644312039273,6.01722622261898,3.71435586640654,4.06180331827025,11.0186237458849,4.41400877553267,4.16134185809148,4.91200853465936,6.14435929476508,3.55579341389526,5.73429009051356,5.1294029169288,5.60122206224381,6.84017537770627,8.23087537861028,5.18312112841531,5.75281442321041,9.58988963769102,2.9058171022862,5.59304032555758,9.95151206607703,9.66457378942286,5.49615658235129,8.28272314889447,5.28974619521139,5.20566317110165,5.1000088024874,5.2890307999594,2.56771471526227,5.41792929120541,8.2485514308283,4.22191248192974,4.18076760394355,3.82490004086774,8.11389467048772,8.17905131591077,2.20512940572033,6.1765196159511,5.64754846416467,7.00670902696149,4.02765634906512,4.14404501418002,3.22816913193604,2.18199137644284,6.17377233089113,4.03767675198414,13.1038052247289,2.19622347217905,4.68070673320595,12.1949138405277,8.54480269571011,4.85111956334843,6.70336942540735,3.23983016542715,5.13082252805444,5.14034177125895,3.4500631319645,7.69852037593398,7.66067049651481,4.16704555356684,4.64433437519586,7.29709139509208,8.19689822731976,11.9751925513851,3.54835361661994,3.89538081803005,5.36146734662152,6.12853671472484,6.23729711901194,3.18961479193869,4.49869589427826,5.76699781603703,6.79504390544921,7.83808323775473,7.76370178578931,3.41926767683594,3.27150688906948,7.56221751278802,8.57238196888134,3.0765656184776,5.31089267521916,3.79480934458552,7.74123456631936,4.04293995118258,9.45300780752185,6.72875943280427,5.35280044337538,2.15342431043033,9.00869311350449,8.30744889962753,8.49287308892036,3.43574809492756,6.13125665675564,9.04021143433454,3.29155021747036,7.35193441805941,7.93653368794213,5.51273094986878,3.38505308966638,2.17589265177759,5.28359279669062,3.47787799463508,5.70752638327164,12.3440437363526,8.19775479403202,10.0806903838118,5.9589068571708,12.2163422772414,2.96748610500741,7.20615636174274,6.34709075641611,6.90605193626859,5.84570188576078,3.45223828038286,8.28021204179474,8.07741844411617,6.46258440661766,6.47332011707804,5.77997972475852,4.98712218243283,3.7878154328551,4.45010616191702,4.75073481008442,4.94080420237503,4.67071100284309,7.27182797493035,7.63637295804752,7.05061070885306,3.30625540738865,3.32740983130141,5.48648934067196,13.4942731235184,2.66508048593565,3.73431560512329,8.54873951859126,3.93630090207988,3.51387025872032,6.03884431177219,13.2520796624539,3.47724256999982,2.38089690325795,7.06417115042977,2.31287956003781,4.60300305335662,5.80900906296062,8.5280212845338,7.44065156091036,7.37113842821828,2.48071561825698,8.27551743348859,7.62851209755008,14.8463629750269,1.97366155087844,11.3385820582077,12.9235625000801,4.86997860978972,4.67229728246753,6.39106356800049,7.19006181092422,4.83047630071042,5.85611253081715,5.20524797573404,2.95765269217928,4.36396317148357,7.09467564481347,10.9468053627988,2.50978020482316,3.52717687279868,6.71782276292188,9.15259518023441,2.68857447805955,10.0808514960569,8.03574389469412,5.79714672725919,4.1872049557106,11.9288445669464,8.10968839913708,1.77864080725759,5.60584129153289,1.92835903620831,13.4832090703276,5.85409752740415,3.55878047647453,6.09871429579707,5.45548827523139,6.94343519310369,5.27509422952383,4.94982694067812,10.471718557911,1.77057226461722,3.69962266030213,5.59224209088963,7.66538495869249,4.20035415007028,7.66037258134326,8.39006483678768,3.41869365885651,8.36740667317747,10.2783276977061,6.70907111542578,3.22267743708372,3.94077915551577,4.11403066964048,7.12254337694263,2.65517135856564,3.26947338757178,4.34293168807362,6.8627027165066,6.27606257247508,3.21584070637301,13.2155117170111,8.20594013328869,4.12458883918245,13.1723796744834,6.14505378032772,11.1283872136079,5.13853537074475,6.79394165269215,5.1593727890658,3.494845791221,5.76450590113332,10.1590680869197,5.42034807894333,6.89824348598303,6.90982287851876,6.71198773190657,5.86697282937759,3.05912935538379,7.45018667041063,5.77763943802571,6.02237525913843,4.44486789665648,8.43899300884028,9.89980957197258,2.13917081686202,9.04758331562325,5.21589097754136,5.05051795371087,6.19232575758405,9.34085189994595,7.29999158070182,6.0360161689356,5.28295115985372,12.9050616162865,5.29128883361962,5.33917562620091,1.65183035925921,6.50515769496072,10.3273944312599,4.18491510991607,6.70390599756346,6.05609544102602,6.83143185227753,8.05545860819656,7.53064725709318,6.05514510681038,6.77985263169223,5.5998540044362,5.82729095356518,4.90532890949783,2.05819896885312,4.31627755871944,4.97274607016806,5.19008822765649,5.61323506069641,6.42173147122194,8.37088732788796,8.00653418538846,4.26151440996175,3.5610062690827,11.4881692078432,2.11242270358537,9.47990149815404,6.7336211984959,5.55430353064164,2.2263654184052,4.62282884499259,2.46503220986232,6.19639933253168,5.19919117910693,4.51674152090613,5.95862919168961,5.79547393573955,5.0125526342321,6.31453717410042,3.63827247163645,2.94742708415586,4.07036706162421,1.47647754913847,3.57712328263973,7.44637152383954,3.16190215467574,5.75208828843793,4.10255336743796,4.81862201715808,3.79939241194872,5.17243280082671,3.06406946393343,11.9053579343422,7.81508667499838,5.98551989978803,7.85494766404866,2.12513112441248,4.43488977253895,6.44611493373454,2.11948116009652,9.20208149946354,3.31366556168537,4.50709565424868,3.28603074670195,4.8929953822012,5.3657171341465,7.73829687257827,5.85321148073022,6.20349342057683,4.39997866283304,8.03774019789768,4.70706577894645,4.21495196258795,6.54380798571769,9.69078065348202,5.51482371040456,8.21135544965855,4.47816186016272,8.6936333631899,4.47511363819238,3.3045496790252,4.00066954789961,5.80997389686452,3.25730377969715,5.29120351391087,3.17282161593051,8.72179661748884,6.26631351938951,3.86933963749373,13.5564464662075,4.63895771438481,4.00235872916829,6.94127902865297,5.65073634548882,6.41508657595473,6.6214554939705,9.41747685659003,8.41032195911151,5.69966980297061,8.19375435617369,2.8817762300048,4.13312527405593,8.44950812841548,6.07520666698793,3.72358613076008,4.76270422283332,5.72918987950143,1.3358861774612,14.2288509876231,5.71310921498087,3.25797679434852,10.5094867242265,6.1070129862946,4.37606154054595,8.43333585480916,6.50298869700406,5.66632544088042,6.71147112350744,5.12376474745983,4.40387660693527,5.18996592723948,2.85248380353141,5.80619480255206,5.37665868177875,8.26819279705691,2.55067216666738,5.44285401170707,5.79445997583341,7.11685652729147,3.96329857357491,3.62366770330987,4.69514392893429,6.29455202808252,5.25986377888816,4.81058812846268,3.50950231930442,5.94934007549484,3.47524774674799,5.00686028347549,4.4708858046076,4.06790804231522,4.82345501446795,5.42292053762581,2.80645729401069,9.30989593398334,8.38700932596938,7.33669059721859,4.82647866672544,6.08220143251275,4.4179595473059,13.5705876270001,3.71981640181635,3.86848052062754,5.59163526301393,2.69206767991973,4.42967389685432,10.8852822442574,5.72351672914615,3.07801483382221,9.99441275712819,4.41124510578886,2.86392022717056,5.09673008147755,4.26574401574091,8.27245343520375,8.19764468442208,2.98352798268172,1.75769488964269,5.43054098103716,7.95757358478887,4.02827269189121,5.16018809793742",
            height=150,
            help="Enter numbers separated by commas or spaces",
            label_visibility="collapsed"
        )
        if data_input:
            data = parse_data(data_input)
            if data is not None and len(data) > 0:
                st.success(f"Loaded {len(data)} data points")
            else:
                st.error("Invalid data format")
    
    # CSV file upload
    else:
        uploaded_file = st.file_uploader("Upload CSV file", type=['csv'])
        if uploaded_file is not None:
            try:
                df = pd.read_csv(uploaded_file)
                
                # Show dataframe preview
                st.markdown("**Preview:**")
                st.dataframe(df.head(), use_container_width=True)
                
                # Let user select column
                column = st.selectbox("Select data column:", df.columns)
                data = df[column].dropna().values
                st.success(f"Loaded {len(data)} data points from '{column}'")
            except Exception as e:
                st.error(f"Error reading file: {e}")

with config_col:
    st.markdown("<p style='font-weight:500; font-size:1.6rem; color:#e94560; margin-top:1.5rem; margin-bottom:1.5rem; border-left:4px solid #e94560; padding-left:1rem; letter-spacing:2px;'>Statistics</p>", unsafe_allow_html=True)
    
    # Display data statistics
    if data is not None and len(data) > 0:
        st.markdown("**Data Statistics:**")
        stat_col1, stat_col2 = st.columns(2)
        with stat_col1:
            st.metric("Count", len(data))
            st.metric("Mean", f"{np.mean(data):.3f}")
            st.metric("Std Dev", f"{np.std(data):.3f}")
        with stat_col2:
            st.metric("Min", f"{np.min(data):.3f}")
            st.metric("Max", f"{np.max(data):.3f}")
            st.metric("Median", f"{np.median(data):.3f}")
    else:
        st.info("Enter or upload data to see statistics")

st.markdown("---")

# ============================================================================
# AUTOMATIC FITTING SECTION
# ============================================================================

if data is not None and len(data) > 0:
    tab1, tab2 = st.tabs(["Automatic Fitting", "Manual Fitting"])
    
    # Tab 1: Automatic Fitting
    with tab1:
        st.markdown("<p style='font-weight:500; font-size:1.6rem; color:#e94560; margin-top:1.5rem; margin-bottom:1.5rem; border-left:4px solid #e94560; padding-left:1rem; letter-spacing:2px;'>Automatic Distribution Fitting</p>", unsafe_allow_html=True)
        
        # Create layout: controls on left, visualization on right
        control_col, viz_col = st.columns([1, 2])
        
        with control_col:
            # Distribution selection
            selected_dist = st.selectbox(
                "Select distribution:",
                list(DISTRIBUTIONS.keys()),
                help="Choose a distribution to fit to your data",
                key='auto_dist'
            )
            
            st.markdown("---")
            
            # Fit the distribution
            dist_info = DISTRIBUTIONS[selected_dist]
            dist_obj = dist_info['dist']
            
            with st.spinner(f"Fitting {selected_dist} distribution..."):
                params = fit_distribution(data, dist_obj)
            
            if params is not None:
                st.markdown("<p style='font-weight:500; font-size:1.1rem; color:#f0f0f0; margin-bottom:0.5rem;'>Fitted Parameters</p>", unsafe_allow_html=True)
                param_names = dist_info['params']
                
                # Create a nice table for parameters
                param_data = []
                for i, (name, value) in enumerate(zip(param_names, params)):
                    param_data.append({'Parameter': name, 'Value': f'{value:.6f}'})
                
                st.table(pd.DataFrame(param_data))
                
                st.markdown("---")
                
                # Display fit quality metrics
                quality_metrics = calculate_fit_quality(data, dist_obj, params)
                st.markdown("<p style='font-weight:500; font-size:1.1rem; color:#f0f0f0; margin-bottom:0.5rem;'>Fit Quality</p>", unsafe_allow_html=True)
                
                metric_col1, metric_col2 = st.columns(2)
                with metric_col1:
                    st.metric("MSE", f"{quality_metrics['MSE']:.5f}", label_visibility="visible")
                    st.metric("KS Stat", f"{quality_metrics['KS Statistic']:.5f}", label_visibility="visible")
                with metric_col2:
                    st.metric("Max Err", f"{quality_metrics['Max Error']:.5f}", label_visibility="visible")
                    st.metric("p-value", f"{quality_metrics['KS p-value']:.5f}", label_visibility="visible")
                
                # Interpretation
                if quality_metrics['KS p-value'] > 0.05:
                    st.success("Good fit (p > 0.05)")
                else:
                    st.warning("Poor fit (p < 0.05)")
            else:
                st.error("Failed to fit distribution.")
        
        with viz_col:
            if params is not None:
                # Plot
                st.markdown("<p style='font-weight:500; font-size:1.1rem; color:#f0f0f0; margin-bottom:0.5rem;'>Visualization</p>", unsafe_allow_html=True)
                fig, ax = plt.subplots(figsize=(10, 7))
                plot_distribution(data, dist_obj, params, selected_dist, ax)
                st.pyplot(fig)
                plt.close()
                
                # Author credit
                st.markdown("<p style='text-align:right; color:#7f8c8d; font-size:0.85rem; margin-top:0.5rem;'>Built by Prisca Chien 21178781</p>", unsafe_allow_html=True)
            else:
                st.info("Select a distribution to see the fitted results")
    
    # Tab 2: Manual Fitting
    with tab2:
        st.markdown("<p style='font-weight:500; font-size:1.6rem; color:#e94560; margin-top:1.5rem; margin-bottom:1.5rem; border-left:4px solid #e94560; padding-left:1rem; letter-spacing:2px;'>Manual Distribution Fitting</p>", unsafe_allow_html=True)
        st.markdown("Adjust the parameters manually using sliders and see the fit in real-time")
        
        # Create layout: controls on left, visualization on right
        control_col, viz_col = st.columns([1, 2])
        
        with control_col:
            # Distribution selection
            manual_dist = st.selectbox(
                "Select distribution:",
                list(DISTRIBUTIONS.keys()),
                key='manual_dist',
                help="Choose a distribution to fit manually"
            )
            
            dist_info = DISTRIBUTIONS[manual_dist]
            dist_obj = dist_info['dist']
            param_names = dist_info['params']
            
            # Get automatic fit as starting point
            auto_params = fit_distribution(data, dist_obj)
            
            st.markdown("---")
            
            # Create sliders for each parameter
            st.markdown("<p style='font-weight:500; font-size:1.1rem; color:#f0f0f0; margin-bottom:0.5rem;'>Adjust Parameters</p>", unsafe_allow_html=True)
            
            manual_params = []
            
            # Determine reasonable ranges for sliders
            data_min, data_max = np.min(data), np.max(data)
            data_range = data_max - data_min
            data_std = np.std(data)
            
            for i, param_name in enumerate(param_names):
                # Set default value from auto-fit if available
                default_val = auto_params[i] if auto_params is not None else 1.0
                
                # Set reasonable ranges based on parameter type
                if param_name in ['loc']:
                    min_val = data_min - data_range
                    max_val = data_max + data_range
                    step = 0.1
                    default_val = round(default_val, 1)
                elif param_name in ['scale']:
                    min_val = 0.01
                    max_val = data_range * 2
                    step = 0.1
                    default_val = max(0.1, round(default_val, 1))
                elif param_name in ['a', 'b', 'c', 's', 'df']:
                    min_val = 0.1
                    max_val = 10.0
                    step = 0.1
                    default_val = max(0.1, min(10.0, default_val))
                else:
                    min_val = 0.1
                    max_val = 10.0
                    step = 0.1
                    default_val = max(0.1, min(10.0, default_val))
                
                value = st.slider(
                    param_name,
                    min_value=float(min_val),
                    max_value=float(max_val),
                    value=float(default_val),
                    step=float(step),
                    format="%.2f" if param_name in ['loc', 'scale'] else "%.3f"
                )
                manual_params.append(value)
            
            st.markdown("---")
            
            # Display fit quality metrics in lower left
            st.markdown("<p style='font-weight:500; font-size:1.1rem; color:#f0f0f0; margin-bottom:0.5rem;'>Fit Quality</p>", unsafe_allow_html=True)
            
            try:
                quality_metrics = calculate_fit_quality(data, dist_obj, manual_params)
                
                metric_col1, metric_col2 = st.columns(2)
                with metric_col1:
                    st.metric("MSE", f"{quality_metrics['MSE']:.5f}", label_visibility="visible")
                    st.metric("KS Stat", f"{quality_metrics['KS Statistic']:.5f}", label_visibility="visible")
                with metric_col2:
                    st.metric("Max Err", f"{quality_metrics['Max Error']:.5f}", label_visibility="visible")
                    st.metric("p-value", f"{quality_metrics['KS p-value']:.5f}", label_visibility="visible")
                    
            except Exception as e:
                st.error(f"Invalid parameters: {e}")
        
        with viz_col:
            # Plot
            st.markdown("<p style='font-weight:500; font-size:1.1rem; color:#f0f0f0; margin-bottom:0.5rem;'>Visualization</p>", unsafe_allow_html=True)
            try:
                fig, ax = plt.subplots(figsize=(10, 7))
                plot_distribution(data, dist_obj, manual_params, manual_dist, ax)
                st.pyplot(fig)
                plt.close()
                
                # Author credit
                st.markdown("<p style='text-align:right; color:#7f8c8d; font-size:0.85rem; margin-top:0.5rem;'>Built by Prisca Chien 21178781</p>", unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Unable to plot: {e}")

else:
    # No data loaded
    st.info("Please enter or upload data using the sidebar to get started")
    
    # Show example
    st.markdown("---")
    st.markdown("<p style='font-weight:500; font-size:1.6rem; color:#e94560; margin-top:1.5rem; margin-bottom:1.5rem; border-left:4px solid #e94560; padding-left:1rem; letter-spacing:2px;'>Example Usage</p>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Manual Entry:**")
        st.code("5.2 6.1 5.8 7.2 6.5 5.9 6.8 7.1", language=None)
        st.markdown("Or use commas:")
        st.code("5.2, 6.1, 5.8, 7.2, 6.5, 5.9", language=None)
    
    with col2:
        st.markdown("**CSV Format:**")
        st.code("""value
5.2
6.1
5.8
7.2
6.5""", language=None)
