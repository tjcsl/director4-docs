---
Title: Node.js
...

# Node.js

Here's a simple Node.js server to get you started, using Express:

```node
var express = require("express");
var app = express();

var listener = app.listen(process.env.PORT || 8080, process.env.HOST || "0.0.0.0", function() {
    console.log("Express server started");
});
```

If you save this as `public/index.js` and run `npm i express` in the terminal, it should work with the default `run.sh` template from the Node.js images. You can add routes, static files, templates, etc. as necessary.

### Database access

After [setting up a database](/databases/quick-start.md), see either the [PostgreSQL Node setup instructions](/databases/postgresql.md#node) or the [MySQL Node setup instructions](/databases/mysql.md#node), as appropriate.
