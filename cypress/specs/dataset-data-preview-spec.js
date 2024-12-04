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
  });
});
