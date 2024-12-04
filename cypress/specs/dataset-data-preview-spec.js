describe("Dataset data preview page", () => {
  context("When visiting the dataset data preview page", () => {
    beforeEach(() => {
      cy.visit("http://127.0.0.1:8000/");
      cy.get('a[data-testid="dataset"]').first().click();
      cy.get('span[data-testid="versions-dropdown"]').click();
      cy.get('a[data-testid="version"]').last().click();
      cy.get('a[data-testid="dataset-table-link"]').first().click();
    });

    it("Loads the navbar component", () => {
      cy.get('[data-testid="navbar"]').should("exist");
    });

    it("Loads dataset data preview header successfully", () => {
      cy.get('[data-testid="dataset-data-preview-header-container"]').should(
        "exist"
      );
      cy.get('[data-testid="dataset-data-preview-header"]').should("exist");
    });

    it("Has columns metadata", () => {
      cy.get('[data-testid="data-columns-metadata"]').should("exist").click();
      cy.get("body").then(($body) => {
        if ($body.find('a[data-testid="data-columns-metadata"]').length > 0) {
          cy.get('table[data-testid="metadata-table"]').should("exist");
          cy.get('th[data-testid="metadata-column"]').should("exist");
          cy.get('th[data-testid="metadata-description"]').should("exist");
        } else {
          cy.get('table[data-testid="metadata-table"').should("not.exist");
          cy.get('[data-module="govuk-notification-banner"]').should("exist");
        }
      });
    });

    it("Shows the download data link", () => {
      cy.get('a[data-module="govuk-button"]').should("exist");
    });

    it("Should display the corret number of rows", () => {
      //   cy.get(".row-count")
      //     .its("length")
      //     .then((rowCount) => {
      cy.get('p[data-testid="row-count"]').should("contain", "236 rows");
      // });
    });

    it.only("Should display the table or report table", () => {
      cy.get('table[data-testid="data-table"]').should("exist");
      cy.get(".data-preview-headers").should("exist");
      cy.get(".data-preview-body")
        .should("exist")
        .should("have.length.greaterThan", 0);
    });
  });
});
