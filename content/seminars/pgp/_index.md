+++
title = "PGP Key-Signing Party"
author = "Matt Soucy"
outputs = ["Reveal"]
+++

# PGP Key-Signing Party

- Presented by Matthew Soucy <git@msoucy.me>
- Inspiration, guidance, and some slides by Ralph Bean

```
4096R/B2370F0C 2013-04-20
33A9 6558 38DE 94B9 B85B  A0DC 7996 734F B237 0F0C
```

![Creative Commons Share-Alike](https://i.creativecommons.org/l/by-sa/4.0/88x31.png)

---

# What is GPG (wikipedia quote time)

---

*Pretty Good Privacy (PGP)* is a data encryption and decryption program that provides cryptographic privacy and authentication for data communication.
PGP is often used for signing, encrypting, and decrypting texts, e-mails, files, directories, and even whole disk partitions.

GNU Privacy Guard (GnuPG or GPG) is a GPL Licensed alternative to the PGP suite of cryptographic software.

---

# Why use GPG?

---

- Signing communications
  - Your friend receives a fraudulent email from your address, asking them to give another person access to a shared project with proprietary information.
    If you usually sign with GPG, and this email is not signed, then your friend is more likely to notice that something is wrong.

---

- Encrypting communications
  - You are a sysadmin and you need to email someone a password.
    Do it in plaintext? **NO**.
	Encrypt the message using the *public key* of the *recipient*.

---

- Signing Data
  - Uploading tarballs of project releases, you sign with a personal key first to show others that this release is legitimate.
    Some projects use a project-specific key shared by all release managers.

---

- Encrypting Data
  - Sometimes you need to share a dump of some proprietary information with another person, but it should not be put online.
    Encrypt with the *public key* of the *recepient* so that only they can read the file.

---

# Visualizing the Web of Trust

---

```bash
gpg --list-sigs --keyring ~/.gnupg/pubring.gpg | \
	sig2dot > ~/.gnupg/pubring.dot
neato -Tps ~/.gnupg/pubring.dot > ~/.gnupg/pubring.ps
convert ~/.gnupg/pubring.ps ~/.gnupg/pubring.gif
eog ~/.gnupg/pubring.gif
```

---

# What signing another key means

---

It means that you trust that the key belongs to the person that it says it does.

It does *not* mean that you trust that person.

If you receive an executable from somebody you don't know, but I've signed their key,
it does *not* mean that I trust that they would not do anything malicious.
It merely means "I trust that this person is actually the person who sent this to you".

---

# Creating your key

---

Before you can sign any keys, you need a key of your own to sign *with*.

You can do this with:

```bash
gpg --gen-key
```

---

Your key is stored in ~/.gnupg/
To check your key, run the following:

```bash
gpg --fingerprint 'your@email.here'
```

Your **fingerprint** is a short identifier that represents your key.
My output:

```
pub   096R/B2370F0C 2013-04-20
	  Key fingerprint = 33A9 6558 38DE 94B9 B85B  A0DC 7996 734F B237 0F0C
uid                  Matthew Soucy <msoucy@csh.rit.edu>
uid                  Matthew Soucy <mas5997@rit.edu>
sub   4096R/2FD2F40B 2013-04-20
```

---

# Sending your key

---

In order for other people to verify that a key belongs to you, and to sign it, you send it to a keyserver.

This is your ***public*** key. Your private key should, as you might expect, stay private.

```bash
gpg --keyserver hkp://subkeys.pgp.net --send-key KEYNAME
# So for my example:
gpg --keyserver hkp://subkeys.pgp.net --send-key B2370F0C
```

---

The keyservers all synchronize, so in practice it doesn't matter which server you use.
However, since many people here just made their keys now, it's better to all use the same server
so that there are no delays or timing problems.

You're able to add email addresses to your key later on.

---

# Quick recap

---

- Signing a key is a sign of trust of **IDENTITY**, not **CHARACTER**
- Keys can be used to sign or encrypt data and communications
- By being part of the Web of Trust, you help verify identities
- Key signing is a great way to meet people at conferences
- NEVER sign a key belonging to someone you have not met face-to-face
- NEVER sign a key if you have not verified that person's identity.

---

# Key Signing Parties

---

A key signing party is a way for a bunch of people to sign each others' keys.
This helps build their web of trust.

Everyone here should have a key generated at this point.

---

# Identification

---

To verify someone's identity, one should
Peoples' preferred forms of ID may differ, but typically the following are used:

- Passport (Any variety)
- Driver's license
- School ID (Least-preferred, least-secure)

---

# Steps in a party

---

- The other person verifies that the key on the list is their key.
- You receive their key from the server
- You verify their identification
- You sign the key using your key
- You email the key to the email address listed in the key
- They send the key back to the keyserver

---

# The party, on a computer

---

The typical flow for these commands looks like this:

```bash
# Using my key as an example:
# Download their key
gpg --keyserver hkp://subkeys.pgp.net --recv-keys B2370F0C
# Sign the key
gpg --sign-key B2370F0C
# Create an updated key that includes your signature
# Email the resulting file to the email address
gpg --armor --output B2370F0C.signed-by.YOUR_KEY.asc --export B2370F0C
# Import the key that you received
gpg --import YOUR_KEY.signed-by.B2370F0C.asc
# Verify all signatures
gpg --list-sigs YOUR_KEY
# Send your newly-signed key to the server
gpg --send-keys YOUR_KEY
```

---

# Using keys

---

You can use tools such as KGPG to manage keys.

Many mail clients allow for pgp signing and encrypting, possibly with plugins:

- Thunderbird (OpenPGP)
- K-9 Mail (Android, integrates with APG

---

# Happy encrypting
