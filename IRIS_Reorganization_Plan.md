# IRIS Environmental AI - Repository Reorganization Plan
====================================================

## 🚨 Critical Issues to Address

### 1. **Massive File Problem**
- `voice_environmental_agent_modern_refactored.py` (47KB, 1,135 lines) - UNACCEPTABLE
- Violates single responsibility principle
- Impossible to maintain or debug

### 2. **Structural Problems**
- `code_storage/` contains important files in wrong location
- Multiple duplicate/legacy files
- Import path issues with `sys.path.append()`
- No proper package structure

### 3. **Missing Core Components**
- No dedicated `smart_monitor.py` (embedded in massive file)
- No `message_generators.py`
- Poor separation of concerns

## 🎯 Target Clean Structure

```
IRIS-Environmental-AI/
├── README.md                    # IRIS-focused documentation
├── requirements.txt             # IRIS dependencies
├── setup.sh                    # IRIS setup script
├── agents/
│   ├── core/
│   │   ├── environmental_agent.py
│   │   ├── smart_monitor.py           # EXTRACT from massive file
│   │   └── message_generators.py      # NEW - extract message logic
│   ├── interfaces/
│   │   ├── llm_interface.py
│   │   └── modern_voice_interface.py
│   └── examples/
│       ├── smart_environmental_ai.py    # NEW - main IRIS system
│       └── voice_environmental_agent_modern_refactored.py  # KEEP for reference
├── arduino/
│   ├── environmental_monitor_combined.ino
│   └── simple_tests/
├── docs/
│   └── IRIS_DEMO_GUIDE.md
└── tools/
    └── voice_selector.py
```

## 🔧 Reorganization Steps

### Step 1: Extract SmartMonitor Class
- Extract `SmartMonitor` class from massive file
- Create `agents/core/smart_monitor.py`
- Remove from main file

### Step 2: Extract Message Generators
- Extract all message generation logic
- Create `agents/core/message_generators.py`
- Centralize all text/voice message creation

### Step 3: Create Main IRIS System
- Create `agents/examples/smart_environmental_ai.py`
- Clean, focused main system
- Remove massive file or keep as reference

### Step 4: Fix Import Structure
- Remove `sys.path.append()` calls
- Create proper `__init__.py` files
- Use relative imports

### Step 5: Clean Up Duplicates
- Remove duplicate files
- Consolidate legacy code
- Move important files from `code_storage/`

## 📋 Implementation Plan

1. **Extract SmartMonitor** (Priority 1)
2. **Create Message Generators** (Priority 1)
3. **Create Main IRIS System** (Priority 1)
4. **Fix Import Structure** (Priority 2)
5. **Clean Up Files** (Priority 3)
6. **Update Documentation** (Priority 3)

## 🎯 Success Criteria

- No file > 500 lines
- Clear separation of concerns
- Proper package structure
- Clean import system
- Focused, maintainable code
- Matches GitHub repository style 