frappe.pages["nr-stock-management"].on_page_load = function (wrapper) {
  var page = frappe.ui.make_app_page({
    parent: wrapper,
    title: "None",
    single_column: true,
  });

  page.set_title("Stock Management");
  let $btn = page.set_primary_action("New", () => console.log("here"));
};
