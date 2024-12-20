const { defineConfig } = require("cypress");

module.exports = defineConfig({
  e2e: {
    baseUrl: "http://localhost:8000",
    specPattern: "cypress/specs",
    supportFile: false,
  },
  fixturesFolder: "cypress/fixtures",
});
