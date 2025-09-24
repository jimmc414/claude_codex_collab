# Implementation Plan Prompt Template

## How to Use This Template

Use this template to create a detailed, actionable implementation plan based on the architecture document that serves as a standalone resource for developers.

## Phase 1: Prerequisites Analysis

Before creating the plan:
1. Read architecture.md thoroughly
2. Identify all components to be built
3. Determine dependencies between components
4. Estimate complexity of each component
5. Plan the implementation order

## Phase 2: Implementation Plan Structure

### 2.1 Setup and Environment

Provide complete instructions for:
- Development environment setup
- Required tools and versions
- Dependencies installation
- Project structure creation

### 2.2 Component Implementation Order

Define the build sequence:
1. Core/foundational components first
2. Components with no dependencies
3. Components with resolved dependencies
4. Integration components last

### 2.3 Detailed Implementation Steps

For each component, provide:
- Step-by-step coding instructions
- Code snippets and examples
- File structure and naming
- Testing approach
- Common pitfalls to avoid

## Implementation Document Format

```markdown
# Implementation Plan: [Project Name]

## 1. Overview
This document provides step-by-step instructions for implementing the [Project Name] system based on the architecture defined in architecture.md.

## 2. Prerequisites

### 2.1 Development Environment
- [ ] [Tool 1] version X.X or higher
- [ ] [Tool 2] version X.X or higher
- [ ] [IDE recommendation]

### 2.2 Required Knowledge
- [Skill 1]: [Level required]
- [Skill 2]: [Level required]

## 3. Project Setup

### Step 1: Initialize Project Structure
\`\`\`bash
mkdir project-name
cd project-name
npm init -y  # or equivalent
\`\`\`

### Step 2: Install Dependencies
\`\`\`bash
npm install express mongoose dotenv
npm install -D nodemon jest
\`\`\`

### Step 3: Create Directory Structure
\`\`\`
project-name/
├── src/
│   ├── controllers/
│   ├── models/
│   ├── services/
│   ├── middleware/
│   └── utils/
├── tests/
├── config/
└── docs/
\`\`\`

## 4. Implementation Phases

### Phase 1: Core Infrastructure (Days 1-2)

#### Task 1.1: Database Connection
**File**: \`src/config/database.js\`
\`\`\`javascript
const mongoose = require('mongoose');

const connectDB = async () => {
    try {
        await mongoose.connect(process.env.MONGODB_URI, {
            useNewUrlParser: true,
            useUnifiedTopology: true
        });
        console.log('MongoDB connected');
    } catch (error) {
        console.error('Database connection failed:', error);
        process.exit(1);
    }
};

module.exports = connectDB;
\`\`\`

**Testing**:
\`\`\`javascript
// tests/database.test.js
describe('Database Connection', () => {
    test('should connect successfully', async () => {
        // Test implementation
    });
});
\`\`\`

#### Task 1.2: [Next task...]

### Phase 2: Business Logic (Days 3-5)

#### Task 2.1: User Model
**File**: \`src/models/User.js\`
\`\`\`javascript
// Complete model implementation
\`\`\`

### Phase 3: API Layer (Days 6-7)

#### Task 3.1: RESTful Routes
**File**: \`src/routes/index.js\`
[Implementation details]

### Phase 4: Frontend (Days 8-10)

#### Task 4.1: Component Structure
[Implementation details]

### Phase 5: Integration (Days 11-12)

#### Task 5.1: Connect Frontend to Backend
[Implementation details]

## 5. Testing Strategy

### 5.1 Unit Tests
\`\`\`bash
npm test -- --coverage
\`\`\`

### 5.2 Integration Tests
[Test scenarios and implementation]

### 5.3 End-to-End Tests
[E2E testing approach]

## 6. Code Quality Checklist

For each component:
- [ ] Code follows style guide
- [ ] Unit tests written and passing
- [ ] Documentation/comments added
- [ ] Error handling implemented
- [ ] Security considerations addressed
- [ ] Performance optimized

## 7. Common Patterns

### 7.1 Error Handling Pattern
\`\`\`javascript
const asyncHandler = (fn) => (req, res, next) => {
    Promise.resolve(fn(req, res, next)).catch(next);
};
\`\`\`

### 7.2 [Other patterns...]

## 8. Troubleshooting Guide

### Issue: [Common Issue 1]
**Solution**: [Step-by-step fix]

### Issue: [Common Issue 2]
**Solution**: [Step-by-step fix]

## 9. Deployment Preparation

### 9.1 Environment Variables
\`\`\`env
NODE_ENV=production
DATABASE_URI=mongodb://...
JWT_SECRET=...
\`\`\`

### 9.2 Build Process
\`\`\`bash
npm run build
npm run start:prod
\`\`\`

## 10. Verification Steps

After implementation:
- [ ] All routes respond correctly
- [ ] Database operations work
- [ ] Authentication/authorization functioning
- [ ] Error handling works properly
- [ ] Performance meets requirements
- [ ] Security measures in place
```

## Code Examples Requirements

For each significant piece of functionality:
1. Provide complete, runnable code
2. Include error handling
3. Add inline comments for complex logic
4. Show test examples
5. Demonstrate usage

## Dependency Management

Specify:
- Exact versions for critical dependencies
- Installation order if relevant
- Configuration requirements
- Environment variables needed

## Progressive Implementation

Structure tasks so that:
1. Each phase produces working code
2. System can be tested incrementally
3. Dependencies are resolved naturally
4. Rollback is possible at any phase

## Interactive Flow

1. Read architecture.md completely
2. Identify implementation challenges
3. Create logical phase breakdown
4. Generate detailed task list
5. Provide code for each task
6. Include testing for each component
7. Add troubleshooting for common issues
8. Ensure standalone usability of document
