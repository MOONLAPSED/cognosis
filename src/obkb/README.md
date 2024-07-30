# Obsidian-Markdown Specification:

## Special symbols:

To include a copyright symbol:

`&copy;`

This will be rendered as: ©

Writing `AT&T` in Markdown can be encoded:

`AT&amp;T`

This will be rendered as: AT&T

### Inline HTML

Markdown supports inline HTML. This means that HTML tags will be processed correctly within a Markdown document. However, angle brackets used outside HTML tags are treated differently:

- **Using angle brackets as delimiters for HTML tags:**

  Writing HTML tags like `<div>`:

  `<div>`

  Markdown will treat these as HTML tags.

- **Using angle brackets for comparisons:**

  Writing `4 < 5`:

  `4 < 5`

  Markdown will translate this to:

  `4 &lt; 5`

  This will be rendered as: 4 < 5

### Code Spans and Blocks

When using code spans (inline code) and code blocks, Markdown automatically encodes special characters. This allows you to write about HTML code without having to manually escape every special character:

- **Using angle brackets and ampersands in code spans and blocks:**

  Writing in a code span: `` `4 < 5 & 6 > 3` `` will remain exactly as you type it:

  `4 < 5 & 6 > 3`

  Writing in a code block:

  `4 < 5 & 6 > 3`

  This will always render correctly and require no manual escaping of characters.

## 'Properties' of .md files (at the top)

```md
---
title: file_title
link: "[[Link]]" 
linklist: 
  - "[[Link]]" 
  - "[[Link2]]"
---
```

```yaml
---
name: value
---
```

Use "quotation marks" around values where values are `[[double-bracketed-entity]]`(s) to create navigable links in 'Properties' sections.

## Functions and Symlinks

Utilizing an obsidian-markdown code like the following, one can save space while creating associative structure and linkages:

`...defined by a ![[qubit]]`

Rendered:

...defined by a [[qubit]]

This will result in an associative link from the article being edited/rendered to the article we are referencing as the editors, an [[obsidian-markdown symlink]].

#### Results:

### As compared to what, exactly?

- **Classical [bit](app://obsidian.md/bit)**:
    - Represented by a binary value of 0 or 1.
    - In hardware, this can be represented by the presence or absence of an electron in the energy well of a MOSFET transistor.
- **[byte](app://obsidian.md/byte)**:
    - Typically 8 bits, allowing for 256 possible combinations (2^8).
    - Can represent integers from 0 to 255 in an unsigned representation.

#### Or, if rendered:

`![[qubit#As compared to what, exactly?]]`

### Hash tags (#):

In this case, the `qubit` article has been tagged with the label `"As compared to what, exactly?"`. This allows you to create links between related articles and their subsections using these tags, making it easier to navigate and explore your knowledge base.

You can use multiple hash tags on a single line to add multiple labels to an article. For example: `![[qubit#As compared to what, exactly?#In the context of]]`

### Dataview Links

Dataview-Obsidian enables table sim links to all SQL syntax articles:

```dataview
LIST
FROM [[Hash Tags]]
LIMIT 10
```

This lists navigable symlinks to the returned articles, per SQL.
