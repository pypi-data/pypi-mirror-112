# Terality

Terality is a distributed data processing engine for Data Scientists to execute all their Pandas code 100 times faster, even on terabytes of data, by only changing one line of code.
Terality is hosted, so there is no infrastructure to manage, and memory is virtually unlimited.

**Note:** You will need a Terality account to use this package. Contact us on [terality.com](https://www.terality.com/) to get started!

## Setup

Configure your credentials once and for all by calling the `configure` function:

```python
import terality
terality.configure('<YOUR_USER_ID>', '<YOUR_USER_SECRET>')
```

By default, the configuration is written inside a `.terality` directory under the current user's home. You can customize that location through the `TERALITY_HOME` environment variable.
