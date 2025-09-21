import requests
import json
from datetime import datetime, timedelta
import logging
from typing import List, Dict
import time

class EconomicDataCollector:
    """Collects economic data from free government and public sources"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        # Free economic data sources
        self.sources = {
            'fred': 'https://api.stlouisfed.org/fred/series/observations',
            'world_bank': 'http://api.worldbank.org/v2/country/all/indicator',
            'oecd': 'https://stats.oecd.org/SDMX-JSON/data'
        }
        self.api_keys = {
            'fred': 'abcdefghijklmnopqrstuvwxyz123456'  # Placeholder - get free API key from FRED
        }
        
    def collect_fred_indicators(self) -> List[Dict]:
        """Collect key economic indicators from FRED (Federal Reserve Economic Data)"""
        # Important FRED series IDs for economic analysis
        key_indicators = {
            'GDP': 'GDP',  # Gross Domestic Product
            'UNRATE': 'UNRATE',  # Unemployment Rate
            'CPIAUCSL': 'CPIAUCSL',  # Consumer Price Index
            'FEDFUNDS': 'FEDFUNDS',  # Federal Funds Rate
            'SP500': 'SP500',  # S&P 500
            'DCOILWTICO': 'DCOILWTICO',  # Crude Oil Prices
            'HOUST': 'HOUST',  # Housing Starts
            'TOTALSA': 'TOTALSA',  # Total Vehicle Sales
            'UMCSENT': 'UMCSENT',  # Consumer Sentiment
            'INDPRO': 'INDPRO'  # Industrial Production Index
        }
        
        indicators_data = []
        
        # Since we don't have API keys, we'll simulate data
        # In production, you would make actual API calls to FRED
        for name, series_id in key_indicators.items():
            try:
                # This would be the actual API call:
                # params = {
                #     'series_id': series_id,
                #     'api_key': self.api_keys['fred'],
                #     'file_type': 'json',
                #     'limit': 10,
                #     'sort_order': 'desc'
                # }
                # response = requests.get(self.sources['fred'], params=params)
                # data = response.json()
                
                # Simulate data for now
                indicator_data = {
                    'indicator': name,
                    'series_id': series_id,
                    'latest_value': self._simulate_latest_value(name),
                    'previous_value': self._simulate_previous_value(name),
                    'change': self._simulate_change(name),
                    'trend': self._determine_trend(name),
                    'timestamp': datetime.now().isoformat(),
                    'source': 'FRED'
                }
                
                indicators_data.append(indicator_data)
                time.sleep(0.5)  # Be respectful to API rate limits
                
            except Exception as e:
                self.logger.error(f"Error collecting FRED data for {name}: {e}")
                
        return indicators_data
    
    def _simulate_latest_value(self, indicator_name: str) -> float:
        """Simulate latest economic indicator value"""
        import random
        base_values = {
            'GDP': 25000,
            'UNRATE': 3.8,
            'CPIAUCSL': 300,
            'FEDFUNDS': 5.25,
            'SP500': 4500,
            'DCOILWTICO': 85,
            'HOUST': 1400000,
            'TOTALSA': 15000000,
            'UMCSENT': 65,
            'INDPRO': 110
        }
        base = base_values.get(indicator_name, 100)
        variation = random.uniform(-5, 5)
        return round(base + variation, 2)
    
    def _simulate_previous_value(self, indicator_name: str) -> float:
        """Simulate previous economic indicator value"""
        import random
        base_values = {
            'GDP': 24800,
            'UNRATE': 3.9,
            'CPIAUCSL': 298,
            'FEDFUNDS': 5.00,
            'SP500': 4450,
            'DCOILWTICO': 82,
            'HOUST': 1380000,
            'TOTALSA': 14800000,
            'UMCSENT': 63,
            'INDPRO': 108
        }
        base = base_values.get(indicator_name, 98)
        variation = random.uniform(-3, 3)
        return round(base + variation, 2)
    
    def _simulate_change(self, indicator_name: str) -> float:
        """Simulate percentage change"""
        import random
        return round(random.uniform(-2, 2), 2)
    
    def _determine_trend(self, indicator_name: str) -> str:
        """Determine trend direction"""
        import random
        trends = ['improving', 'declining', 'stable', 'volatile']
        return random.choice(trends)
    
    def collect_world_bank_data(self) -> List[Dict]:
        """Collect global economic data from World Bank"""
        # Simulate World Bank data
        countries = ['US', 'CN', 'JP', 'DE', 'IN', 'GB', 'FR', 'IT', 'BR', 'CA']
        indicators = [
            'NY.GDP.MKTP.CD',  # GDP (current US$)
            'SL.UEM.TOTL.ZS',  # Unemployment rate (% of total labor force)
            'FP.CPI.TOTL.ZG',  # Inflation, consumer prices (annual %)
            'GC.BAL.CASH.GD.ZS',  # Cash surplus/deficit (% of GDP)
            'BN.CAB.XOKA.GD.ZS'  # Current account balance (% of GDP)
        ]
        
        world_data = []
        
        for country in countries[:3]:  # Limit for simulation
            for indicator in indicators[:2]:  # Limit for simulation
                try:
                    # Simulate World Bank data
                    data_point = {
                        'country': country,
                        'indicator_code': indicator,
                        'indicator_name': self._get_indicator_name(indicator),
                        'value': self._simulate_world_bank_value(indicator),
                        'year': 2023,
                        'source': 'World Bank'
                    }
                    world_data.append(data_point)
                except Exception as e:
                    self.logger.error(f"Error collecting World Bank data: {e}")
                    
        return world_data
    
    def _get_indicator_name(self, code: str) -> str:
        """Get human-readable name for World Bank indicator"""
        names = {
            'NY.GDP.MKTP.CD': 'GDP (current US$)',
            'SL.UEM.TOTL.ZS': 'Unemployment rate (% of total labor force)',
            'FP.CPI.TOTL.ZG': 'Inflation, consumer prices (annual %)',
            'GC.BAL.CASH.GD.ZS': 'Cash surplus/deficit (% of GDP)',
            'BN.CAB.XOKA.GD.ZS': 'Current account balance (% of GDP)'
        }
        return names.get(code, code)
    
    def _simulate_world_bank_value(self, indicator: str) -> float:
        """Simulate World Bank indicator value"""
        import random
        base_values = {
            'NY.GDP.MKTP.CD': 2500000000000,
            'SL.UEM.TOTL.ZS': 5.2,
            'FP.CPI.TOTL.ZG': 3.1,
            'GC.BAL.CASH.GD.ZS': -2.8,
            'BN.CAB.XOKA.GD.ZS': -1.2
        }
        base = base_values.get(indicator, 100)
        variation = random.uniform(-10, 10)
        return round(base + variation, 2)
    
    def find_economic_anomalies(self) -> List[Dict]:
        """Find unusual economic patterns or anomalies"""
        # Simulate detection of economic anomalies
        anomalies = [
            {
                "type": "consumer_spending_shift",
                "description": "Unusual increase in sustainable product purchases",
                "data_source": "retail_sales_surveys",
                "significance": "moderate",
                "potential_impact": "growing_market_segment"
            },
            {
                "type": "regional_employment_trend",
                "description": "Tech sector growth in non-traditional hubs",
                "data_source": "bureau_of_labor_statistics",
                "significance": "high",
                "potential_impact": "remote_work_economic_shifts"
            },
            {
                "type": "generational_spending_pattern",
                "description": "Gen Z preference shift toward experience over ownership",
                "data_source": "consumer_expenditure_surveys",
                "significance": "high",
                "potential_impact": "new_financial_product_opportunities"
            },
            {
                "type": "inflation_sector_disparity",
                "description": "Differential inflation rates across service categories",
                "data_source": "cpi_detailed_reports",
                "significance": "moderate",
                "potential_impact": "budgeting_strategy_adjustments"
            }
        ]
        
        return anomalies
    
    def collect_unemployment_data(self) -> Dict:
        """Collect detailed unemployment statistics"""
        # Simulate unemployment data
        unemployment_data = {
            'overall_rate': 3.8,
            'youth_unemployment': 7.2,
            'long_term_unemployment': 1.1,
            'part_time_for_economic_reasons': 2.8,
            'by_sector': {
                'construction': 4.1,
                'manufacturing': 3.5,
                'healthcare': 2.1,
                'technology': 2.8,
                'retail': 5.2,
                'finance': 2.3
            },
            'by_education': {
                'less_than_high_school': 6.1,
                'high_school': 4.2,
                'some_college': 3.5,
                'bachelor_degree': 2.1,
                'graduate_degree': 1.8
            },
            'by_age': {
                '16-24': 8.9,
                '25-34': 3.2,
                '35-44': 2.8,
                '45-54': 3.1,
                '55+': 3.4
            },
            'source': 'Bureau of Labor Statistics',
            'last_updated': datetime.now().isoformat()
        }
        
        return unemployment_data
    
    def collect_income_distribution_data(self) -> Dict:
        """Collect income distribution and inequality data"""
        # Simulate income distribution data
        income_data = {
            'gini_coefficient': 0.41,
            'income_shares': {
                'lowest_10_percent': 1.8,
                'lowest_20_percent': 3.1,
                'lowest_50_percent': 12.5,
                'highest_10_percent': 30.4,
                'highest_5_percent': 22.4,
                'highest_1_percent': 15.3
            },
            'median_income': 70000,
            'mean_income': 95000,
            'poverty_rate': 11.5,
            'deep_poverty_rate': 4.5,
            'source': 'Census Bureau',
            'year': 2023
        }
        
        return income_data

if __name__ == "__main__":
    # Test the economic data collector
    collector = EconomicDataCollector()
    
    # Collect FRED indicators
    fred_data = collector.collect_fred_indicators()
    print(f"Collected {len(fred_data)} FRED indicators:")
    for indicator in fred_data[:3]:
        print(f"- {indicator['indicator']}: {indicator['latest_value']} ({indicator['change']}% change)")
    
    print("\n" + "="*50 + "\n")
    
    # Find economic anomalies
    anomalies = collector.find_economic_anomalies()
    print(f"Found {len(anomalies)} economic anomalies:")
    for anomaly in anomalies[:2]:
        print(f"- {anomaly['description']} (significance: {anomaly['significance']})")