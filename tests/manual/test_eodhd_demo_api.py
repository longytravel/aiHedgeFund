"""
Manual test to validate EODHD API response format using demo key.

This test uses EODHD's free demo API key to fetch real data for AAPL.US
and verify that our EODHDProvider correctly parses the response.

Demo key limitations:
- Only works for: AAPL.US, TSLA.US, VTI.US, AMZN.US, BTC-USD.CC, EURUSD.FOREX
- Full access to all data types (fundamentals, prices, estimates)

Run this test:
    python tests/manual/test_eodhd_demo_api.py
"""

import asyncio
import sys
from pathlib import Path
from datetime import datetime, timezone, timedelta
import json
import os

# Fix Windows console encoding for emojis
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from backend.app.data_sources.providers.eodhd_provider import EODHDProvider


async def test_demo_api():
    """Test EODHD API with demo key to validate response format."""

    print("=" * 80)
    print("EODHD Demo API Validation Test")
    print("=" * 80)
    print()

    # Get API key from environment or use demo
    api_key = os.getenv("EODHD_API_KEY", "demo")

    provider = EODHDProvider(
        api_key=api_key,
        tickers=["AAPL.US"],  # Demo key only works with specific tickers
        cache_ttl_hours=0,  # Disable cache for testing
        rate_limit_per_day=100000  # Standard limit
    )

    print("Testing with demo API key...")
    print("Ticker: AAPL.US (Apple Inc.)")
    print()

    # Test 1: Fetch fundamentals
    print("-" * 80)
    print("TEST 1: Fetch Fundamentals")
    print("-" * 80)
    try:
        fundamentals = await provider.fetch_fundamentals("AAPL.US")

        if fundamentals:
            print("✅ SUCCESS - Fundamentals fetched")
            print()
            print("Response structure:")
            print(f"  - general: {list(fundamentals.get('general', {}).keys())[:5]}...")
            print(f"  - highlights: {list(fundamentals.get('highlights', {}).keys())[:5]}...")
            print(f"  - key_metrics: {list(fundamentals.get('key_metrics', {}).keys())[:5]}...")
            print()
            print("Sample data:")
            if fundamentals.get('general'):
                print(f"  Company: {fundamentals['general'].get('name')}")
                print(f"  Sector: {fundamentals['general'].get('sector')}")
                print(f"  Exchange: {fundamentals['general'].get('exchange')}")
            if fundamentals.get('key_metrics'):
                print(f"  P/E Ratio: {fundamentals['key_metrics'].get('pe_ratio')}")
                print(f"  Market Cap: ${fundamentals['key_metrics'].get('market_cap'):,.0f}" if fundamentals['key_metrics'].get('market_cap') else "  Market Cap: N/A")
            print()

            # Save sample response for inspection
            with open('tests/manual/eodhd_fundamentals_sample.json', 'w') as f:
                json.dump(fundamentals, f, indent=2)
            print("  Full response saved to: tests/manual/eodhd_fundamentals_sample.json")

        else:
            print("❌ FAILED - No fundamentals data returned")

    except Exception as e:
        print(f"❌ ERROR - {type(e).__name__}: {e}")

    print()

    # Test 2: Fetch historical prices
    print("-" * 80)
    print("TEST 2: Fetch Historical Prices (Last 30 days)")
    print("-" * 80)
    try:
        to_date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        from_date = (datetime.now(timezone.utc) - timedelta(days=30)).strftime("%Y-%m-%d")

        prices = await provider.fetch_historical_prices("AAPL.US", from_date, to_date)

        if prices and prices.get('prices'):
            print("✅ SUCCESS - Historical prices fetched")
            print()
            print(f"  Date range: {from_date} to {to_date}")
            print(f"  Data points: {prices.get('data_points', 0)}")
            print(f"  Latest price: ${prices.get('latest_price', 0):.2f}")
            print(f"  30-day change: {prices.get('price_change_30d', 0):.2f}%")
            print()
            print("  Sample price data (first 3 days):")
            for price in prices['prices'][:3]:
                print(f"    {price['date']}: Open=${price['open']:.2f}, Close=${price['close']:.2f}, Volume={price['volume']:,}")
            print()

            # Save sample response
            with open('tests/manual/eodhd_prices_sample.json', 'w') as f:
                json.dump(prices, f, indent=2)
            print("  Full response saved to: tests/manual/eodhd_prices_sample.json")

        else:
            print("❌ FAILED - No price data returned")

    except Exception as e:
        print(f"❌ ERROR - {type(e).__name__}: {e}")

    print()

    # Test 3: Fetch company profile
    print("-" * 80)
    print("TEST 3: Fetch Company Profile")
    print("-" * 80)
    try:
        profile = await provider.fetch_company_profile("AAPL.US")

        if profile:
            print("✅ SUCCESS - Company profile fetched")
            print()
            print("  Company Information:")
            print(f"    Name: {profile.get('name')}")
            print(f"    Sector: {profile.get('sector')}")
            print(f"    Industry: {profile.get('industry')}")
            print(f"    Country: {profile.get('country')}")
            print(f"    Employees: {profile.get('employees'):,}" if profile.get('employees') else "    Employees: N/A")
            print(f"    Website: {profile.get('website')}")
            print()

            # Save sample response
            with open('tests/manual/eodhd_profile_sample.json', 'w') as f:
                json.dump(profile, f, indent=2)
            print("  Full response saved to: tests/manual/eodhd_profile_sample.json")

        else:
            print("❌ FAILED - No profile data returned")

    except Exception as e:
        print(f"❌ ERROR - {type(e).__name__}: {e}")

    print()

    # Test 4: Fetch analyst estimates
    print("-" * 80)
    print("TEST 4: Fetch Analyst Estimates")
    print("-" * 80)
    try:
        estimates = await provider.fetch_analyst_estimates("AAPL.US")

        if estimates and estimates.get('total_analysts', 0) > 0:
            print("✅ SUCCESS - Analyst estimates fetched")
            print()
            print("  Analyst Coverage:")
            print(f"    Total Analysts: {estimates.get('total_analysts', 0)}")
            print(f"    Consensus: {estimates.get('consensus', 'N/A')}")
            print(f"    Target Price: ${estimates.get('target_price', 0):.2f}" if estimates.get('target_price') else "    Target Price: N/A")
            print()
            print("  Ratings Breakdown:")
            print(f"    Strong Buy: {estimates.get('strong_buy', 0)}")
            print(f"    Buy: {estimates.get('buy', 0)}")
            print(f"    Hold: {estimates.get('hold', 0)}")
            print(f"    Sell: {estimates.get('sell', 0)}")
            print(f"    Strong Sell: {estimates.get('strong_sell', 0)}")
            print()

            # Save sample response
            with open('tests/manual/eodhd_estimates_sample.json', 'w') as f:
                json.dump(estimates, f, indent=2)
            print("  Full response saved to: tests/manual/eodhd_estimates_sample.json")

        elif estimates:
            print("⚠️  WARNING - Analyst data fetched but no coverage available")
        else:
            print("❌ FAILED - No analyst data returned")

    except Exception as e:
        print(f"❌ ERROR - {type(e).__name__}: {e}")

    print()

    # Test 5: Fetch all signals (end-to-end test)
    print("-" * 80)
    print("TEST 5: End-to-End Signal Generation")
    print("-" * 80)
    try:
        signals = await provider.fetch()

        if signals:
            print(f"✅ SUCCESS - Generated {len(signals)} signals")
            print()
            print("  Signal Types:")
            for signal in signals:
                print(f"    - {signal.signal_type} (score: {signal.score}, confidence: {signal.confidence:.2f})")
            print()

            # Validate signal format
            for signal in signals:
                assert signal.ticker == "AAPL.US", f"Incorrect ticker: {signal.ticker}"
                assert 0 <= signal.score <= 100, f"Invalid score: {signal.score}"
                assert 0.0 <= signal.confidence <= 1.0, f"Invalid confidence: {signal.confidence}"
                assert signal.timestamp.tzinfo is not None, "Timestamp not timezone-aware"
                assert signal.source == "eodhd_fundamental", f"Invalid source: {signal.source}"

            print("  ✅ All signals validated (ticker, score, confidence, timestamp, source)")

        else:
            print("❌ FAILED - No signals generated")

    except Exception as e:
        print(f"❌ ERROR - {type(e).__name__}: {e}")

    print()

    # Summary
    print("=" * 80)
    print("VALIDATION SUMMARY")
    print("=" * 80)
    print()
    print("✅ If all tests passed, our EODHDProvider correctly:")
    print("   1. Connects to EODHD API")
    print("   2. Parses fundamentals, prices, profiles, and estimates")
    print("   3. Generates valid Signal objects")
    print("   4. Handles US market data format")
    print()
    print("📝 Next Steps:")
    print("   1. Review saved JSON files in tests/manual/ to verify response structure")
    print("   2. When ready to test LSE stocks (VOD.L, BP.L, etc.):")
    print("      - Sign up for free EODHD plan (20 calls/day)")
    print("      - Or upgrade to paid plan ($19.99+)")
    print("   3. The code should work identically for LSE stocks")
    print()
    print("💡 Note: UK-specific features (pence/pounds conversion) can't be tested")
    print("   with demo key, but the logic is simple and well-tested in unit tests.")
    print()

    # Close HTTP client
    await provider.close()


if __name__ == "__main__":
    # Create manual test directory if it doesn't exist
    Path("tests/manual").mkdir(parents=True, exist_ok=True)

    # Run the test
    asyncio.run(test_demo_api())
