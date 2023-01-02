+++
title = "Packaging Firefox Addons"
author = "Matt Soucy"
outputs = ["Reveal"]
date = "October 30, 2014"
+++

---

# Let's make an addon!

Addons are really `.zip` files with a special set of files:

- `chrome.manifest` - describes the contents
- `install.rdf` - Addon metadata

---

# Content

Put the content in a `content` directory.

It uses a `.xul` file to tell it:

- Which files to use
- The order to load them in
- Specification for new toolbar buttons

---

# JS Content

Implement the actual features

---

# Packaging it up

`zip` is your friend

---

# Submission

- Upload the `.xpi`
- Tag with the license
- Submit any deobfuscated/pre-generation code
