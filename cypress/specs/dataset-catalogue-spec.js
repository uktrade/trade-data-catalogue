describe("Dataset catalogue page", () => {
  context("When visiting the dataset catalogue page", () => {
    it("Loads page successfully", () => {
      cy.request("http://127.0.0.1:8000/").its("status").should("eq", 200);
    });

    beforeEach(() => {
      cy.visit("http://127.0.0.1:8000/");
    });

    it("Loads dataset catalogue header successfully", () => {
      cy.get('[data-testid="dataset-catalogue-header-container"]').should(
        "exist"
      );
      cy.get('[data-testid="dataset-catalogue-header"]').should("exist");
    });

    it("Loads dataset successfully", () => {
      cy.get('[data-testid="dataset"]').should("exist");
    });

    it("Loads dataset number of versions successfully", () => {
      cy.get('[data-testid="dataset-versions"]').should("exist");
    });
  });
});
