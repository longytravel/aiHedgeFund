"""Initial schema for Epic 1

Revision ID: 001_initial
Revises:
Create Date: 2025-11-23 12:58:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '001_initial'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create stocks table
    op.create_table('stocks',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('ticker', sa.String(length=10), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('sector', sa.String(length=100), nullable=True),
    sa.Column('market_cap', sa.Numeric(precision=15, scale=2), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('ticker')
    )
    op.create_index(op.f('ix_stocks_id'), 'stocks', ['id'], unique=False)
    op.create_index(op.f('ix_stocks_ticker'), 'stocks', ['ticker'], unique=True)

    # Create signals table
    op.create_table('signals',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('stock_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('stock_ticker', sa.String(length=10), nullable=False),
    sa.Column('type', sa.String(length=50), nullable=False),
    sa.Column('strength', sa.Integer(), nullable=False),
    sa.Column('agent_id', sa.String(length=50), nullable=False),
    sa.Column('timestamp', sa.DateTime(timezone=True), nullable=False),
    sa.Column('data', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.ForeignKeyConstraint(['stock_id'], ['stocks.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_signals_agent_id'), 'signals', ['agent_id'], unique=False)
    op.create_index(op.f('ix_signals_id'), 'signals', ['id'], unique=False)
    op.create_index(op.f('ix_signals_stock_id'), 'signals', ['stock_id'], unique=False)
    op.create_index(op.f('ix_signals_stock_ticker'), 'signals', ['stock_ticker'], unique=False)
    op.create_index(op.f('ix_signals_timestamp'), 'signals', ['timestamp'], unique=False)
    op.create_index(op.f('ix_signals_type'), 'signals', ['type'], unique=False)

    # Create analysis_results table
    op.create_table('analysis_results',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('stock_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('stock_ticker', sa.String(length=10), nullable=False),
    sa.Column('agent_id', sa.String(length=50), nullable=False),
    sa.Column('recommendation', sa.String(length=20), nullable=False),
    sa.Column('score', sa.Integer(), nullable=False),
    sa.Column('confidence', sa.String(length=10), nullable=False),
    sa.Column('reasoning', sa.Text(), nullable=False),
    sa.Column('key_metrics', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('risks', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('timestamp', sa.DateTime(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['stock_id'], ['stocks.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_analysis_results_agent_id'), 'analysis_results', ['agent_id'], unique=False)
    op.create_index(op.f('ix_analysis_results_id'), 'analysis_results', ['id'], unique=False)
    op.create_index(op.f('ix_analysis_results_stock_id'), 'analysis_results', ['stock_id'], unique=False)
    op.create_index(op.f('ix_analysis_results_stock_ticker'), 'analysis_results', ['stock_ticker'], unique=False)
    op.create_index(op.f('ix_analysis_results_timestamp'), 'analysis_results', ['timestamp'], unique=False)

    # Create portfolio_positions table
    op.create_table('portfolio_positions',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('stock_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('entry_date', sa.DateTime(timezone=True), nullable=False),
    sa.Column('entry_price', sa.Float(), nullable=False),
    sa.Column('quantity', sa.Integer(), nullable=False),
    sa.Column('stop_loss', sa.Float(), nullable=True),
    sa.Column('target', sa.Float(), nullable=True),
    sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['stock_id'], ['stocks.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_portfolio_positions_id'), 'portfolio_positions', ['id'], unique=False)
    op.create_index(op.f('ix_portfolio_positions_stock_id'), 'portfolio_positions', ['stock_id'], unique=False)

    # Create watchlist_entries table
    op.create_table('watchlist_entries',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('stock_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('trigger_type', sa.String(), nullable=True),
    sa.Column('trigger_value', sa.Float(), nullable=True),
    sa.Column('thesis', sa.Text(), nullable=True),
    sa.Column('expiry_date', sa.DateTime(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['stock_id'], ['stocks.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_watchlist_entries_id'), 'watchlist_entries', ['id'], unique=False)
    op.create_index(op.f('ix_watchlist_entries_stock_id'), 'watchlist_entries', ['stock_id'], unique=False)

    # Create research_queue table
    op.create_table('research_queue',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('stock_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('score', sa.Float(), nullable=True),
    sa.Column('status', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['stock_id'], ['stocks.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_research_queue_id'), 'research_queue', ['id'], unique=False)
    op.create_index(op.f('ix_research_queue_status'), 'research_queue', ['status'], unique=False)
    op.create_index(op.f('ix_research_queue_stock_id'), 'research_queue', ['stock_id'], unique=False)

    # Create trades table
    op.create_table('trades',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('stock_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('action', sa.String(), nullable=False),
    sa.Column('price', sa.Float(), nullable=False),
    sa.Column('quantity', sa.Integer(), nullable=False),
    sa.Column('timestamp', sa.DateTime(timezone=True), nullable=False),
    sa.Column('outcome', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['stock_id'], ['stocks.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_trades_id'), 'trades', ['id'], unique=False)
    op.create_index(op.f('ix_trades_stock_id'), 'trades', ['stock_id'], unique=False)
    op.create_index(op.f('ix_trades_timestamp'), 'trades', ['timestamp'], unique=False)

    # Create reports table
    op.create_table('reports',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('date', sa.Date(), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('stocks_analyzed', sa.Integer(), nullable=True),
    sa.Column('recommendations_count', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('date')
    )
    op.create_index(op.f('ix_reports_date'), 'reports', ['date'], unique=True)
    op.create_index(op.f('ix_reports_id'), 'reports', ['id'], unique=False)

    # Create agent_config table
    op.create_table('agent_config',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('agent_name', sa.String(), nullable=False),
    sa.Column('enabled', sa.Boolean(), server_default=sa.text('true'), nullable=False),
    sa.Column('weight', sa.Float(), server_default=sa.text('1.0'), nullable=False),
    sa.Column('parameters', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('agent_name')
    )
    op.create_index(op.f('ix_agent_config_agent_name'), 'agent_config', ['agent_name'], unique=True)
    op.create_index(op.f('ix_agent_config_id'), 'agent_config', ['id'], unique=False)

    # Create audit_log table
    op.create_table('audit_log',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('action', sa.String(), nullable=False),
    sa.Column('details', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('user_id', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_audit_log_action'), 'audit_log', ['action'], unique=False)
    op.create_index(op.f('ix_audit_log_id'), 'audit_log', ['id'], unique=False)


def downgrade() -> None:
    # Drop tables in reverse order
    op.drop_index(op.f('ix_audit_log_id'), table_name='audit_log')
    op.drop_index(op.f('ix_audit_log_action'), table_name='audit_log')
    op.drop_table('audit_log')

    op.drop_index(op.f('ix_agent_config_id'), table_name='agent_config')
    op.drop_index(op.f('ix_agent_config_agent_name'), table_name='agent_config')
    op.drop_table('agent_config')

    op.drop_index(op.f('ix_reports_id'), table_name='reports')
    op.drop_index(op.f('ix_reports_date'), table_name='reports')
    op.drop_table('reports')

    op.drop_index(op.f('ix_trades_timestamp'), table_name='trades')
    op.drop_index(op.f('ix_trades_stock_id'), table_name='trades')
    op.drop_index(op.f('ix_trades_id'), table_name='trades')
    op.drop_table('trades')

    op.drop_index(op.f('ix_research_queue_stock_id'), table_name='research_queue')
    op.drop_index(op.f('ix_research_queue_status'), table_name='research_queue')
    op.drop_index(op.f('ix_research_queue_id'), table_name='research_queue')
    op.drop_table('research_queue')

    op.drop_index(op.f('ix_watchlist_entries_stock_id'), table_name='watchlist_entries')
    op.drop_index(op.f('ix_watchlist_entries_id'), table_name='watchlist_entries')
    op.drop_table('watchlist_entries')

    op.drop_index(op.f('ix_portfolio_positions_stock_id'), table_name='portfolio_positions')
    op.drop_index(op.f('ix_portfolio_positions_id'), table_name='portfolio_positions')
    op.drop_table('portfolio_positions')

    op.drop_index(op.f('ix_analysis_results_timestamp'), table_name='analysis_results')
    op.drop_index(op.f('ix_analysis_results_stock_ticker'), table_name='analysis_results')
    op.drop_index(op.f('ix_analysis_results_stock_id'), table_name='analysis_results')
    op.drop_index(op.f('ix_analysis_results_id'), table_name='analysis_results')
    op.drop_index(op.f('ix_analysis_results_agent_id'), table_name='analysis_results')
    op.drop_table('analysis_results')

    op.drop_index(op.f('ix_signals_type'), table_name='signals')
    op.drop_index(op.f('ix_signals_timestamp'), table_name='signals')
    op.drop_index(op.f('ix_signals_stock_ticker'), table_name='signals')
    op.drop_index(op.f('ix_signals_stock_id'), table_name='signals')
    op.drop_index(op.f('ix_signals_id'), table_name='signals')
    op.drop_index(op.f('ix_signals_agent_id'), table_name='signals')
    op.drop_table('signals')

    op.drop_index(op.f('ix_stocks_ticker'), table_name='stocks')
    op.drop_index(op.f('ix_stocks_id'), table_name='stocks')
    op.drop_table('stocks')
