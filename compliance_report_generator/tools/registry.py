from tools.news_tool import get_compliance_news
from tools.compliance_lookup import lookup_compliance
from tools.compliance_lookup_tool import get_compliance_score
from tools.risk_calculator import calculate_risk
from tools.summary_filter_tool import summarize_and_filter

TOOLS = [
    get_compliance_news,
    lookup_compliance,
    get_compliance_score,
    calculate_risk,
    summarize_and_filter
]
