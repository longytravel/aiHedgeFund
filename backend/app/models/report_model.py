from sqlalchemy import Column, Date, String, Text, Integer

from app.models.base_model import BaseModel

class Report(BaseModel):
    __tablename__ = "reports"

    date = Column(Date, unique=True, nullable=False, index=True) # Date of the report
    content = Column(Text, nullable=False) # Full content of the report
    stocks_analyzed = Column(Integer, nullable=True)
    recommendations_count = Column(Integer, nullable=True)

    def __repr__(self):
        return f"<Report(date='{self.date}', stocks_analyzed={self.stocks_analyzed})>"
