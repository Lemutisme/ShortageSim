#!/usr/bin/env python3
"""
Setup Test Script for Drug Shortage Simulation
==============================================

This script tests the basic setup and configuration before running the full simulation.
"""

import asyncio
import sys
import argparse
from pathlib import Path

# Add the src directory to the path
sys.path.append(str(Path(__file__).parent))

try:
    from configs import SimulationConfig
    print("✅ Configuration module imported successfully")
except ImportError as e:
    print(f"❌ Failed to import configuration: {e}")
    sys.exit(1)

def test_api_key_setup(providers=None):
    """Test API key configuration for specified providers."""
    print("\n🔑 Testing API Key Setup...")
    
    if providers is None:
        providers = ['openai']
    
    config = SimulationConfig()
    
    provider_configs = {
        'openai': (config.openai_api_key, 'OPENAI_API_KEY', './keys/openai.txt'),
        'anthropic': (config.anthropic_api_key, 'ANTHROPIC_API_KEY', './keys/anthropic.txt'),
        'gemini': (config.gemini_api_key, 'GEMINI_API_KEY', './keys/gemini.txt'),
        'deepseek': (config.deepseek_api_key, 'DEEPSEEK_API_KEY', './keys/deepseek.txt')
    }
    
    results = {}
    for provider in providers:
        if provider not in provider_configs:
            print(f"⚠️  Unknown provider: {provider}")
            results[provider] = False
            continue
            
        api_key, env_var, key_file = provider_configs[provider]
        if api_key and len(api_key) > 10:
            print(f"✅ {provider.capitalize()} API key found: {api_key[:8]}...{api_key[-4:]}")
            results[provider] = True
        else:
            print(f"⚠️  No {provider.capitalize()} API key found - will use mock responses")
            print(f"   To use real LLM calls:")
            print(f"   1. Set environment variable: export {env_var}='your-key-here'")
            print(f"   2. Or create file: {key_file} with your API key")
            results[provider] = False
    
    # Return True if at least one provider has a key
    return any(results.values())

def test_provider_libraries(providers=None):
    """Test if required libraries are available for specified providers."""
    print("\n📦 Testing Provider Libraries...")
    
    if providers is None:
        providers = ['openai']
    
    libraries = {
        'openai': ('openai', 'openai'),
        'anthropic': ('anthropic', 'anthropic'),
        'gemini': ('google.generativeai', 'google-generativeai'),
        'deepseek': ('openai', 'openai')  # Uses OpenAI-compatible API
    }
    
    results = {}
    for provider in providers:
        if provider not in libraries:
            print(f"⚠️  Unknown provider: {provider}")
            results[provider] = False
            continue
            
        import_name, package_name = libraries[provider]
        try:
            if import_name == 'openai':
                import openai
                version = getattr(openai, '__version__', 'unknown')
                print(f"✅ {provider.capitalize()} library available (version: {version})")
                results[provider] = True
            elif import_name == 'anthropic':
                import anthropic
                version = getattr(anthropic, '__version__', 'unknown')
                print(f"✅ {provider.capitalize()} library available (version: {version})")
                results[provider] = True
            elif import_name == 'google.generativeai':
                import google.generativeai as genai
                version = getattr(genai, '__version__', 'unknown')
                print(f"✅ {provider.capitalize()} library available (version: {version})")
                results[provider] = True
        except ImportError:
            print(f"❌ {provider.capitalize()} library not installed")
            print(f"   Install with: pip install {package_name}")
            results[provider] = False
    
    # Return True if at least one library is available
    return any(results.values())

async def test_mock_llm_call():
    """Test that mock LLM calls work."""
    print("\n🤖 Testing Mock LLM Calls...")
    
    try:
        from base import BaseAgent
        from configs import SimulationConfig
        
        # Create a simple test agent
        class TestAgent(BaseAgent):
            async def collect_and_analyze(self, context):
                return {"test": "analysis"}
            
            async def decide(self, state_json):
                return {"test": "decision"}
            
            def get_default_decision(self, context):
                return {"test": "default"}
        
        config = SimulationConfig()
        agent = TestAgent("test_agent", config)
        
        # Test mock response
        mock_response = agent._mock_response()
        print(f"✅ Mock response generated: {len(mock_response)} characters")
        
        # Test JSON parsing
        import json
        parsed = json.loads(mock_response)
        print(f"✅ Mock response is valid JSON with keys: {list(parsed.keys())}")
        
        return True
        
    except Exception as e:
        print(f"❌ Mock LLM test failed: {e}")
        return False

async def test_simulation_setup(providers=None):
    """Test simulation initialization with specified providers."""
    print("\n🏭 Testing Simulation Setup...")
    
    if providers is None:
        providers = ['openai']
    
    results = {}
    for provider in providers:
        try:
            from simulator import SimulationCoordinator
            from configs import SimulationConfig
            
            config = SimulationConfig(
                n_manufacturers=2,  # Small test
                n_periods=1,        # Single period
                llm_temperature=0.1,
                llm_provider=provider
            )
            
            print(f"\n  Testing with {provider.capitalize()} provider...")
            print(f"  ✅ Configuration created: {config.n_manufacturers} manufacturers, {config.n_periods} periods")
            
            # Test coordinator initialization
            coordinator = SimulationCoordinator(config)
            print(f"  ✅ Simulation coordinator created successfully")
            
            # Check that agents are initialized
            print(f"  ✅ {len(coordinator.environment.manufacturers)} manufacturers initialized")
            print(f"  ✅ Buyer agent: {coordinator.environment.buyer.agent_id}")
            print(f"  ✅ FDA agent: {coordinator.environment.fda.agent_id}")
            
            results[provider] = True
            
        except Exception as e:
            print(f"  ❌ Simulation setup with {provider.capitalize()} failed: {e}")
            results[provider] = False
    
    # Return True if at least one provider works
    return any(results.values())

async def run_mini_simulation(providers=None):
    """Run a minimal simulation to test end-to-end functionality with specified providers."""
    print("\n🚀 Running Mini Simulation (1 period, 2 manufacturers)...")
    
    if providers is None:
        providers = ['openai']
    default_model_dict = {
        'openai': 'gpt-4o',
        'anthropic': 'claude-sonnet-4-5-20250929',
        'gemini': 'gemini-2.0-flash',
        'deepseek': 'deepseek-chat'
    }
    
    results = {}
    for provider in providers:
        try:
            from simulator import SimulationCoordinator
            from configs import SimulationConfig
            
            print(f"\n  Testing with {provider.capitalize()} provider, {default_model_dict[provider]} model...")
            
            config = SimulationConfig(
                n_manufacturers=2,
                n_periods=1,
                disruption_probability=0.0,  # No disruptions for test
                llm_temperature=0.1,
                llm_provider=provider,
                llm_model= default_model_dict[provider]
            )
            
            # Check if API key is available for this provider
            provider_keys = {
                'openai': config.openai_api_key,
                'anthropic': config.anthropic_api_key,
                'gemini': config.gemini_api_key,
                'deepseek': config.deepseek_api_key
            }
            
            api_key = provider_keys.get(provider)
            if not api_key or len(api_key) < 10:
                print(f"  ⚠️  Skipping {provider.capitalize()} - no API key found (will use mock responses)")
                results[provider] = None  # Skipped
                continue
            
            coordinator = SimulationCoordinator(config)
            sim_results = await coordinator.run_simulation()
            
            print(f"  ✅ Mini simulation with {provider.capitalize()} completed successfully!")
            
            # Print key results
            metrics = sim_results['summary_metrics']
            print(f"     Peak shortage: {metrics['peak_shortage_percentage']:.1%}")
            print(f"     Total manufacturer profit: {metrics['total_manufacturer_profit']:.3f}")
            print(f"     Buyer cost: {sim_results['buyer_total_cost']:.3f}")
            
            # Print logging info
            logging_info = sim_results.get('logging_session', {})
            if logging_info:
                print(f"     Simulation ID: {logging_info.get('simulation_id', 'unknown')}")
                print(f"     Log events: {logging_info.get('total_events', 0)}")
            
            results[provider] = True
            
        except Exception as e:
            print(f"  ❌ Mini simulation with {provider.capitalize()} failed: {e}")
            import traceback
            traceback.print_exc()
            results[provider] = False
    
    # Return True if at least one provider succeeded
    successful = [r for r in results.values() if r is True]
    return len(successful) > 0

def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description='Test setup for Drug Shortage Simulation',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
        Examples:
        # Test OpenAI (default)
        python test_setup.py
        
        # Test multiple providers
        python test_setup.py --providers openai gemini
        
        # Test all providers
        python test_setup.py --providers openai anthropic gemini deepseek
        
        # Test Anthropic and DeepSeek
        python test_setup.py --providers anthropic deepseek

        Available providers: openai, anthropic, gemini, deepseek
        """
    )
    parser.add_argument(
        '--providers',
        nargs='+',
        choices=['openai', 'anthropic', 'gemini', 'deepseek'],
        default=['openai'],
        help='Providers to test (default: openai)'
    )
    return parser.parse_args()

async def main():
    """Run all tests."""
    args = parse_args()
    providers = args.providers
    
    print("🧬 Drug Shortage Simulation - Setup Test")
    print("=" * 50)
    
    print(f"Testing providers: {', '.join(providers)}")
    
    tests = [
        ("API Key Setup", test_api_key_setup, providers),
        ("Provider Libraries", test_provider_libraries, providers),
        ("Mock LLM Calls", test_mock_llm_call, None),  # Mock test doesn't need providers
        ("Simulation Setup", test_simulation_setup, providers),
        ("Mini Simulation", run_mini_simulation, providers)
    ]
    
    results = []
    
    for test_name, test_func, test_providers in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        
        try:
            if asyncio.iscoroutinefunction(test_func):
                if test_providers is not None:
                    result = await test_func(test_providers)
                else:
                    result = await test_func()
            else:
                if test_providers is not None:
                    result = test_func(test_providers)
                else:
                    result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print(f"\n{'='*50}")
    print("📊 Test Summary:")
    print(f"{'='*50}")
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:<20} {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("\n🎉 All tests passed! Your simulation is ready to run.")
        print("   Use: python main.py")
    else:
        print(f"\n⚠️  {len(results) - passed} tests failed. Please fix the issues above.")
        if passed >= 3:  # If basic functionality works
            print("   Basic functionality appears to work - you can try running with mock responses.")

if __name__ == "__main__":
    asyncio.run(main())