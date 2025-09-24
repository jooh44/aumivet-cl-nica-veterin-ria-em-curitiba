# Design Review Slash Command

## Command: `/design-review`

### Purpose
Enable instant, comprehensive design reviews of current code changes using automated analysis and Playwright testing.

### Usage
```
/design-review [scope] [options]
```

### Parameters
- `scope` (optional): Specific area to review
  - `current` - Review current working changes (default)
  - `pr` - Review changes in current PR
  - `component <name>` - Review specific component
  - `page <url>` - Review specific page

### Options
- `--full` - Complete 7-phase review process
- `--quick` - Quick visual check only  
- `--accessibility` - Focus on accessibility compliance
- `--responsive` - Focus on responsive design
- `--performance` - Focus on performance metrics

### Implementation Process

1. **Change Detection**
   ```bash
   git diff --name-only HEAD~1 HEAD
   git status --porcelain
   ```

2. **File Analysis**
   - Identify modified frontend files
   - Categorize changes (HTML, CSS, JS, components)
   - Detect potential design impact

3. **Automated Review Launch**
   - Initialize Playwright browser instance
   - Load affected pages/components
   - Execute review phases based on scope
   - Capture screenshots and evidence

4. **Report Generation**
   - Structured markdown report
   - Visual evidence attachments
   - Prioritized issue list
   - Actionable recommendations

### Review Phases (Full Mode)

#### Phase 1: Quick Smoke Test
- Load all affected pages
- Check for JavaScript errors
- Verify basic functionality

#### Phase 2: Visual Consistency
- Compare against design principles
- Check color, typography, spacing
- Verify brand guideline compliance

#### Phase 3: Responsive Behavior
- Test across multiple viewports
- Verify layout integrity
- Check touch target sizes

#### Phase 4: Accessibility Audit
- Run automated accessibility tests
- Check keyboard navigation
- Verify screen reader compatibility

#### Phase 5: Interaction Testing
- Test all interactive elements
- Verify form functionality
- Check loading and error states

#### Phase 6: Performance Check
- Measure load times
- Check asset optimization
- Verify critical rendering path

#### Phase 7: Cross-Browser Validation
- Test in major browsers
- Document compatibility issues
- Verify polyfill requirements

### Output Format

```markdown
# Design Review Report
Generated: [timestamp]
Scope: [reviewed scope]
Changes: [number] files modified

## Executive Summary
[Overall assessment and key findings]

## Critical Issues (Blockers)
- [Issue 1 with impact description]
- [Issue 2 with impact description]

## High-Priority Issues
- [Issue 1 with screenshot reference]
- [Issue 2 with screenshot reference]

## Medium-Priority Issues
- [Enhancement suggestions]
- [Code quality improvements]

## Testing Evidence
### Screenshots
- [Before/after comparisons]
- [Cross-device screenshots]
- [Error state captures]

### Playwright Test Results
- [Automated test summaries]
- [Performance metrics]
- [Accessibility scores]

## Recommendations
1. [Prioritized action items]
2. [Implementation suggestions]
3. [Future considerations]
```

### Integration Examples

#### Quick Check After Component Change
```bash
# After modifying a React component
/design-review component Button --quick
```

#### Full PR Review
```bash
# Before submitting PR
/design-review pr --full
```

#### Accessibility Focus
```bash
# Check accessibility compliance
/design-review current --accessibility
```

#### Performance Analysis
```bash
# Focus on performance impact
/design-review page /dashboard --performance
```

### Configuration Options

#### Browser Settings
```javascript
const browserConfig = {
  headless: true,
  viewport: { width: 1440, height: 900 },
  browsers: ['chromium', 'firefox', 'webkit'],
  devices: ['iPhone 12', 'iPad', 'Desktop']
};
```

#### Review Thresholds
```javascript
const thresholds = {
  performance: {
    loadTime: 3000, // ms
    firstPaint: 1500, // ms
    lighthouse: 90 // score
  },
  accessibility: {
    contrast: 4.5, // ratio
    wcag: 'AA' // level
  }
};
```

### Error Handling
- Graceful failure for unreachable URLs
- Timeout handling for slow operations
- Fallback options for browser issues
- Clear error messages with suggestions

### Best Practices
1. Run quick checks frequently during development
2. Use full reviews before PR submission
3. Focus reviews on specific concerns when appropriate
4. Document and track recurring issues
5. Update design principles based on review findings