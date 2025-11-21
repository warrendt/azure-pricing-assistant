# GitHub Copilot Instructions for Azure Seller Assistant

## Project Context

This is an AI-powered Azure pricing solution built with Microsoft Agent Framework. The solution uses a multi-agent workflow to gather requirements, generate Bill of Materials (BOM), calculate pricing, and create proposals.

## Required Reading

**CRITICAL**: Before making any changes to agent code or instructions, you MUST reference the phase-specific documentation:

### Phase 1 (Mock Implementation)
- **`specs/phase1/AGENT_INSTRUCTIONS.md`** - EXACT prompt specifications for all 4 agents using mock/hardcoded responses
- **`specs/phase1/ARCHITECTURE.md`** - Phase 1 architecture with workflow orchestration patterns
- **`specs/phase1/PROGRESS.md`** - Phase 1 implementation tasks and progress tracking

### Phase 2 (Enhanced Implementation)
- **`specs/phase2/AGENT_INSTRUCTIONS.md`** - EXACT prompt specifications for all 4 agents with real API integration
- **`specs/phase2/ARCHITECTURE.md`** - Phase 2 architecture with API integration and intelligent prompting
- **`specs/phase2/PROGRESS.md`** - Phase 2 implementation tasks and progress tracking

### Shared Resources
- **`specs/shared/API_SPEC.md`** - Azure Retail Prices API documentation and Microsoft Agent Framework API patterns (used in Phase 2)

## Agent Implementation Rules

### 1. Agent Instructions Fidelity
When implementing or modifying agent code:
- Determine current phase (Phase 1 or Phase 2) from `specs/phase1/PROGRESS.md` or `specs/phase2/PROGRESS.md`
- Copy agent instructions EXACTLY from the appropriate phase folder:
  - Phase 1: `specs/phase1/AGENT_INSTRUCTIONS.md`
  - Phase 2: `specs/phase2/AGENT_INSTRUCTIONS.md`
- Do NOT paraphrase, summarize, or modify the wording
- Maintain all capitalization, formatting, and emphasis (e.g., "MUST", "IMPORTANT")
- Include all examples and schema specifications exactly as written

### 2. Workflow Orchestration
- Question Agent MUST use `HandoffBuilder` with termination condition detecting "We are DONE!"
- BOM, Pricing, and Proposal agents MUST use `SequentialBuilder`
- Follow the event handling patterns specified in the phase-specific `ARCHITECTURE.md`
- Handle `RequestInfoEvent` and `WorkflowCompletedEvent` as documented

### 3. Data Schemas
- BOM JSON schema MUST match the specification in the phase-specific `AGENT_INSTRUCTIONS.md`
- Required fields: `serviceName`, `sku`, `quantity`, `region`, `armRegionName`, `hours_per_month`
- Pricing output MUST include `items` array and `total_monthly`
- Proposal MUST follow the markdown template structure

### 4. API Integration (Phase 2 Only)
- Use Azure Retail Prices API endpoint: `https://prices.azure.com/api/retail/prices`
- Follow OData filter patterns from `specs/shared/API_SPEC.md`
- Handle errors gracefully (return 0.0 for missing pricing data)
- Implement retry logic for transient failures

### 5. Code Organization
Follow the file structure defined in phase-specific `ARCHITECTURE.md`:
```
src/
├── agents/
│   ├── question_agent.py
│   ├── bom_agent.py
│   ├── pricing_agent.py
│   └── proposal_agent.py
└── utils/
    └── pricing_api.py  (Phase 2 only)
```

### 6. Testing Requirements
- All agent changes must be tested end-to-end
- Verify "We are DONE!" termination for Question Agent
- Validate JSON schema compliance for BOM output
- Test pricing API integration with real calls
- Review proposal output quality

## Common Tasks

### Creating/Modifying an Agent
1. Check current phase from `specs/phase1/PROGRESS.md` or `specs/phase2/PROGRESS.md`
2. Read the agent specification in the phase-specific `ARCHITECTURE.md`
3. Copy instructions from the phase-specific `AGENT_INSTRUCTIONS.md`
4. Implement using `AzureAIAgentClient.create_agent()`
5. Use exact instruction text in the `instructions` parameter

### Updating Agent Instructions
1. Update the phase-specific `AGENT_INSTRUCTIONS.md` first
2. Then update the agent implementation to use new instructions
3. Test the change end-to-end
4. Update the phase-specific `PROGRESS.md` to mark task complete

### Adding API Integration (Phase 2 Only)
1. Reference `specs/shared/API_SPEC.md` for endpoint and schema
2. Implement in `src/utils/pricing_api.py`
3. Register as tool for Pricing Agent
4. Test with real API calls

## Phase-Specific Guidance

### Phase 1: Mock Implementation
- Use hardcoded responses from Phase 1 `AGENT_INSTRUCTIONS.md` sections
- Focus on workflow orchestration and event handling
- Keep complexity minimal
- Verify end-to-end flow works
- No API integration required

### Phase 2: Enhanced Implementation
- Use enhanced instructions from Phase 2 `AGENT_INSTRUCTIONS.md` sections
- Integrate Azure Retail Prices API
- Implement JSON parsing and validation
- Add intelligent prompt engineering
- Test with real API calls

## Quality Standards

### Agent Instructions
- ✅ DO: Copy exact text from phase-specific `AGENT_INSTRUCTIONS.md`
- ✅ DO: Include all schema examples and formatting rules
- ✅ DO: Maintain all caps emphasis and important notes
- ❌ DON'T: Paraphrase or simplify instructions
- ❌ DON'T: Remove examples or schema specifications
- ❌ DON'T: Change formatting or structure

### Code Quality
- Use async/await patterns (Microsoft Agent Framework is async)
- Include type hints for function signatures
- Add error handling for API calls and JSON parsing
- Log important events and errors
- Follow Python PEP 8 style guidelines

### Documentation
- Update phase-specific `PROGRESS.md` when completing tasks
- Add comments for complex logic
- Update phase-specific `ARCHITECTURE.md` if making architectural changes
- Keep API examples in `specs/shared/API_SPEC.md` current

## Termination Signal

**CRITICAL**: The Question Agent MUST output exactly "We are DONE!" (case-sensitive, with exclamation mark) to signal completion. This text:
- Must appear in the agent's final response
- Triggers the workflow termination condition
- Must not appear in intermediate responses
- Is detected by: `any("We are DONE!" in msg.text for msg in conv if msg.role.value == "assistant")`

## Getting Started

When starting work on this project:
1. Read phase-specific `ARCHITECTURE.md` for system overview
2. Check phase-specific `PROGRESS.md` for current phase and next task
3. Reference phase-specific `AGENT_INSTRUCTIONS.md` for exact agent prompts
4. Use `specs/shared/API_SPEC.md` for API integration details

## Questions or Uncertainties

If agent behavior is unclear:
1. Check phase-specific `AGENT_INSTRUCTIONS.md` first - it's the source of truth for agent behavior
2. Review phase-specific `ARCHITECTURE.md` for architectural patterns
3. Consult `specs/shared/API_SPEC.md` for API-specific questions
4. Check phase-specific `PROGRESS.md` for phase-specific requirements

---

**Remember**: The agent instructions in phase-specific `AGENT_INSTRUCTIONS.md` files are carefully crafted prompts. Even small changes in wording can significantly affect agent behavior. Always use the exact text specified for the current phase.
