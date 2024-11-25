describe("Dataset details page", () => {
  context("When visiting a dataset details page", () => {
    beforeEach(() => {
      cy.visit("http://127.0.0.1:8000/");
      cy.get('a[data-testid="dataset"]').first().click();
    });

    it("Loads the navbar component", () => {
      cy.get('[data-testid="navbar"]').should("exist");
    });

    it("Loads dataset details header successfully", () => {
      cy.get('[data-testid="dataset-details-header-container"]').should(
        "exist"
      );
      cy.get('[data-testid="dataset-details-header"]').should("exist");
    });

    it("If it has the tables tab, it has tables", () => {
      cy.get('body').then(($body) => {
        if ($body.find('a[data-testid="tables-tab"]').length > 0) {
          cy.get('a[data-testid="tables-tab"]').should("exist");
          cy.get('a[data-testid="dataset-table-link"]').should("exist");
        } else {
          cy.get('a[data-testid="dataset-table-link"]').should("not.exist");
        }
      });
    });

    it("If it has the reports tab, it has reports", () => {
      cy.get('body').then(($body) => {
        if ($body.find('a[data-testid="reports-tab"]').length > 0) {
          cy.get('a[data-testid="reports-tab"]').should("exist");
          cy.get('a[data-testid="dataset-report-link"]').should("exist");
        } else {
          cy.get('a[data-testid="dataset-report-link"]').should("not.exist");
        }
      });
    });

    it("Loads the previous versions component", () => {
      cy.get('[data-testid="previous-versions-container"]').should("exist");
    });
  });
});
