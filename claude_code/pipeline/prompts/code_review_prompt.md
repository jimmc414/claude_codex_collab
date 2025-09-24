# Code Review Prompt Template

## Instructions for Claude

Perform a comprehensive code review based on implementation requirements and best practices.

## Review Phases

### Phase 1: Automated Checks
Run and analyze results from:
1. Linting tools (ESLint, Pylint, etc.)
2. Type checking (TypeScript, mypy)
3. Security scanning (bandit, npm audit)
4. Test coverage reports
5. Performance profiling

### Phase 2: Manual Review

#### 2.1 Requirements Alignment
- [ ] All functional requirements implemented
- [ ] Non-functional requirements met
- [ ] Acceptance criteria satisfied
- [ ] Edge cases handled

#### 2.2 Code Quality
- [ ] Follows project coding standards
- [ ] Consistent naming conventions
- [ ] DRY principle followed
- [ ] SOLID principles applied
- [ ] Appropriate abstraction levels

#### 2.3 Architecture Compliance
- [ ] Follows defined architecture
- [ ] Components properly separated
- [ ] Dependencies correctly managed
- [ ] Interfaces properly implemented

#### 2.4 Security Review
- [ ] Input validation present
- [ ] Authentication properly implemented
- [ ] Authorization checks in place
- [ ] No sensitive data exposed
- [ ] SQL injection prevention
- [ ] XSS protection
- [ ] CSRF protection

#### 2.5 Performance Review
- [ ] No N+1 queries
- [ ] Appropriate caching used
- [ ] Database queries optimized
- [ ] Async operations handled properly
- [ ] Memory leaks prevented

#### 2.6 Error Handling
- [ ] All exceptions caught appropriately
- [ ] Error messages user-friendly
- [ ] Logging implemented
- [ ] Graceful degradation

#### 2.7 Testing
- [ ] Unit tests comprehensive
- [ ] Integration tests present
- [ ] Test coverage adequate (>80%)
- [ ] Tests are maintainable
- [ ] Edge cases tested

#### 2.8 Documentation
- [ ] Code comments where needed
- [ ] API documentation complete
- [ ] README updated
- [ ] Complex logic explained

## Review Report Format

```markdown
# Code Review Report

## Summary
- **Review Date**: [Date]
- **Reviewer**: Claude AI
- **Project**: [Project Name]
- **Branch**: [Branch Name]
- **Overall Status**: [PASS/FAIL/NEEDS_IMPROVEMENT]

## Automated Checks Results

### Linting
- **Tool**: [ESLint/Pylint/etc.]
- **Issues Found**: [Count]
- **Critical Issues**: [Count]
- **Status**: [PASS/FAIL]

### Type Checking
- **Issues Found**: [Count]
- **Status**: [PASS/FAIL]

### Security Scan
- **High Risk**: [Count]
- **Medium Risk**: [Count]
- **Low Risk**: [Count]
- **Status**: [PASS/FAIL]

### Test Coverage
- **Overall Coverage**: [XX%]
- **Lines Covered**: [X/Y]
- **Branches Covered**: [X/Y]
- **Status**: [PASS/FAIL]

## Manual Review Findings

### Critical Issues
1. **[Issue Title]**
   - **File**: [path/to/file.js:line]
   - **Description**: [What's wrong]
   - **Recommendation**: [How to fix]
   - **Code Example**:
   \`\`\`javascript
   // Current
   [problematic code]

   // Suggested
   [fixed code]
   \`\`\`

### Major Issues
[List major issues with same format]

### Minor Issues
[List minor issues]

### Suggestions for Improvement
[Non-critical suggestions]

## Requirements Traceability

| Requirement | Status | Implementation | Notes |
|-------------|--------|---------------|-------|
| FR-1 | ✅ | src/feature.js:45 | Fully implemented |
| FR-2 | ⚠️ | src/other.js:12 | Partially complete |

## Performance Metrics

- **Load Time**: [X ms]
- **Memory Usage**: [X MB]
- **Database Queries**: [Count]
- **API Response Time**: [X ms]

## Security Checklist

- [x] Input validation
- [x] Authentication
- [ ] Rate limiting (missing)
- [x] Data encryption
- [x] HTTPS only

## Code Quality Metrics

- **Cyclomatic Complexity**: [Average]
- **Code Duplication**: [X%]
- **Maintainability Index**: [Score]

## Recommendations

### Must Fix (Blocking)
1. [Critical issue that must be resolved]

### Should Fix (Important)
1. [Important but non-blocking issue]

### Consider Fixing (Nice to Have)
1. [Minor improvement suggestion]

## Next Steps
1. Address all critical issues
2. Run tests again after fixes
3. Update documentation
4. Request re-review
```

## Review Criteria Thresholds

### Pass Criteria
- No critical security issues
- Test coverage > 80%
- All functional requirements met
- No blocking bugs

### Fail Criteria
- Critical security vulnerabilities
- Test coverage < 60%
- Major functionality missing
- Performance requirements not met

## Interactive Review Process

1. **Initial Scan**: Run all automated tools
2. **Deep Dive**: Examine critical paths
3. **Pattern Check**: Look for anti-patterns
4. **Security Audit**: Check for vulnerabilities
5. **Performance Test**: Verify efficiency
6. **Documentation**: Ensure completeness
7. **Generate Report**: Create comprehensive review
8. **Provide Fixes**: Suggest specific solutions

## Common Issues to Check

### JavaScript/TypeScript
- Promises without error handling
- Memory leaks in event listeners
- Unhandled async errors
- Missing null checks
- Console.logs in production

### Python
- Mutable default arguments
- Missing type hints
- Unclosed file handles
- SQL injection vulnerabilities
- Global variables misuse

### General
- Hardcoded credentials
- Missing rate limiting
- Inadequate logging
- Poor error messages
- Missing input validation