# Contributing to Productivity System Framework

Thank you for your interest in contributing to the Productivity System Framework! This project aims to help people build effective productivity systems, and your contributions can help make that happen.

## Ways to Contribute

There are many ways to contribute to this project:

### 1. 📝 Documentation Improvements

- Fix typos or clarify confusing sections
- Add more examples or use cases
- Improve existing guides
- Translate documentation to other languages
- Add visual diagrams or flowcharts

### 2. 📚 New Content

- Create new templates
- Write additional guides for specific use cases
- Add more examples
- Share your own productivity workflows
- Document integration with other tools

### 3. 🔧 Automation Scripts

- Improve existing scripts
- Add new automation tools
- Create integrations with other platforms
- Fix bugs in scripts
- Add error handling and logging

### 4. 💡 Ideas and Discussions

- Share feedback on what's working or not working
- Propose new features or improvements
- Discuss productivity methodologies
- Share success stories

### 5. 🐛 Bug Reports

- Report issues with scripts or documentation
- Identify broken links or outdated information
- Point out inconsistencies

## Getting Started

### Before You Begin

1. **Read the documentation** - Familiarize yourself with the framework
2. **Check existing issues** - See if someone else has already reported what you found
3. **Review pull requests** - Check if someone is already working on a similar contribution

### Setting Up Your Environment

For script contributions:

```bash
# Fork and clone the repository
git clone https://github.com/YOUR_USERNAME/productivity-system-framework.git
cd productivity-system-framework

# Install dependencies (for Python scripts)
pip install -r requirements.txt

# Create a new branch
git checkout -b feature/your-feature-name
```

## Contribution Guidelines

### Documentation Contributions

**For documentation improvements:**

1. Keep the tone friendly and accessible
2. Use clear, concise language
3. Include practical examples
4. Follow the existing structure and formatting
5. Use Markdown for all documentation

**File naming conventions:**
- Use lowercase with hyphens: `my-new-guide.md`
- Place in appropriate directory (docs/, templates/, examples/)

**Formatting standards:**
- Use ATX-style headers (`#` not underlines)
- Include table of contents for long documents
- Use code blocks with language specification
- Add emojis sparingly for visual appeal

### Template Contributions

**For new templates:**

1. Include clear instructions on how to use the template
2. Provide an example (in /examples directory)
3. Make it adaptable for different use cases
4. Include comments or notes where helpful
5. Test the template yourself before submitting

**Template structure:**
```markdown
# Template Name

[Brief description of what this template is for]

## How to Use
[Step-by-step instructions]

## Template
[The actual template content]

## Examples
[Link to example usage]

## Customization Tips
[How to adapt for different needs]
```

### Script Contributions

**For automation scripts:**

1. Write clear, well-commented code
2. Include a docstring at the top explaining what it does
3. Add setup instructions in comments
4. Handle errors gracefully
5. Test thoroughly before submitting
6. Include requirements (dependencies)

**Script requirements:**
- Python 3.7+ for Python scripts
- Clear variable names
- Error handling
- Environment variable configuration
- Usage examples in comments
- README or docstring with setup instructions

**Example script structure:**
```python
#!/usr/bin/env python3
"""
Script Name

Brief description of what this script does.

Usage:
    python script-name.py [arguments]

Requirements:
    - dependency1
    - dependency2
"""

import required_modules

# Configuration
CONFIG_VAR = os.environ.get("CONFIG_VAR")

# Your code here...

if __name__ == "__main__":
    main()

# Setup Instructions:
# 1. Install dependencies: pip install dependency
# 2. Set environment variables: export VAR=value
# 3. Run: python script-name.py
```

### Example Contributions

**For practical examples:**

1. Use realistic scenarios
2. Show complete workflows, not just fragments
3. Include actual data (anonymized if needed)
4. Explain the context and decision-making
5. Show both successes and challenges

## Pull Request Process

### Before Submitting

1. **Test your changes** - Ensure everything works
2. **Follow the style guide** - Match existing formatting
3. **Update documentation** - If you changed functionality
4. **Keep it focused** - One feature/fix per PR

### Submitting a Pull Request

1. **Create a descriptive title**
   - Good: "Add habit tracking template for shift workers"
   - Bad: "New template"

2. **Write a clear description**
   ```markdown
   ## Description
   [What does this PR do?]

   ## Type of Change
   - [ ] Documentation improvement
   - [ ] New template
   - [ ] Script enhancement
   - [ ] Bug fix
   - [ ] New feature

   ## Testing
   [How did you test this?]

   ## Related Issues
   [Link to any related issues]
   ```

3. **Link related issues** - Reference issue numbers

4. **Be responsive** - Respond to feedback and questions

### Review Process

1. Maintainer will review your PR
2. May request changes or ask questions
3. Once approved, PR will be merged
4. Your contribution will be credited

## Style Guide

### Markdown Style

- Use ATX-style headers: `# Header`
- Use fenced code blocks with language: ` ```python `
- Use consistent bullet styles
- Leave blank line before and after headers
- Use relative links for internal documents

### Writing Style

- Write in second person ("you") for guides
- Use active voice
- Keep paragraphs short (3-5 sentences)
- Use lists for multiple items
- Be encouraging and supportive in tone

### Code Style

**Python:**
- Follow PEP 8
- Use meaningful variable names
- Add docstrings to functions
- Include type hints where helpful
- Keep functions focused and small

**General:**
- Comment complex logic
- Use consistent indentation
- Handle errors appropriately
- Validate user input

## Code of Conduct

### Our Standards

- Be respectful and inclusive
- Welcome newcomers
- Accept constructive criticism gracefully
- Focus on what's best for the community
- Show empathy towards others

### Unacceptable Behavior

- Harassment or discrimination
- Trolling or insulting comments
- Personal or political attacks
- Publishing others' private information
- Any conduct deemed inappropriate

## Questions?

If you have questions:

1. **Check existing documentation** - Your question might be answered
2. **Search issues** - Someone may have asked the same thing
3. **Open a discussion** - For general questions
4. **Open an issue** - For specific problems or suggestions

## Recognition

All contributors will be recognized in the project. Your contributions help make productivity systems more accessible to everyone!

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for contributing to the Productivity System Framework!** 🚀

Your time and effort help others build better systems and live more productive, fulfilling lives.
