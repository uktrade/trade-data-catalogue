describe("Dataset catalogue page", () => {
  it("Loads page successfully", () => {
    cy.request("http://127.0.0.1:8000/").its("status").should("eq", 200);
  });

  it("Loads dataset catalogue header successfully", () => {
    cy.visit("http://127.0.0.1:8000/");
    cy.get('[data-testid="dataset-catalogue-header-container"]').should(
      "exist"
    );
    cy.get('[data-testid="dataset-catalogue-header"]').should("exist");
  });

  it("Loads dataset successfully", () => {
    cy.visit("http://127.0.0.1:8000/");
    cy.get('[data-testid="dataset"]').should("exist");
  });
});
