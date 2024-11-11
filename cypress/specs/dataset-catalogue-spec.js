describe("Dataset catalogue page", () => {
  it("Loads page successfully", () => {
    cy.request("http://127.0.0.1:8000/").its("status").should("eq", 200);
  });
});
