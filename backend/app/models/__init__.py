# flake8: noqa
from app.core.database import Base
from app.models.base_model import BaseModel
from app.models.stock_model import Stock
from app.models.signal_model import Signal
from app.models.analysis_result_model import AnalysisResult
from app.models.portfolio_position_model import PortfolioPosition
from app.models.watchlist_entry_model import WatchlistEntry
from app.models.research_queue_model import ResearchQueue
from app.models.trade_model import Trade
from app.models.report_model import Report
from app.models.agent_config_model import AgentConfig
from app.models.audit_log_model import AuditLog

# For Alembic autogenerate to work, all models must be imported or registered here.
# __all__ = [
#     "Stock", "Signal", "AnalysisResult", "PortfolioPosition", "WatchlistEntry",
#     "ResearchQueue", "Trade", "Report", "AgentConfig", "AuditLog"
# ]
