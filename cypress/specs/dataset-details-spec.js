describe("Dataset details page", () => {
  context("When visiting a dataset details page that has tables", () => {
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

    it("Has the tables tab", () => {
      cy.get('a[data-testid="tables-tab"]').should("exist");
    });

    it("Has tables", () => {
      cy.get('a[data-testid="dataset-table-link"]').should("exist");
    });
  });
});
