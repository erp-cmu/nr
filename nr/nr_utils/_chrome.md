# Testing Sales Process

start-process "chrome.exe" "http://localhost:8000/app/nr-sales-import", '--profile-directory="Default"' &
start-process "chrome.exe" "http://localhost:8000/app/sales-order", '--profile-directory="Default"' &
start-process "chrome.exe" "http://localhost:8000/app/sales-invoice", '--profile-directory="Default"' &
start-process "chrome.exe" "http://localhost:8000/app/payment-entry", '--profile-directory="Default"' &
start-process "chrome.exe" "http://localhost:8000/app/delivery-note", '--profile-directory="Default"' &
start-process "chrome.exe" "http://localhost:8000/app/item", '--profile-directory="Default"' &
start-process "chrome.exe" "http://localhost:8000/app/repost-item-valuation", '--profile-directory="Default"' &
start-process "chrome.exe" "http://localhost:8000/app/customer", '--profile-directory="Default"' &
start-process "chrome.exe" "http://localhost:8000/app/account/view/tree", '--profile-directory="Default"'

# Testing Item

start-process "chrome.exe" "http://localhost:8000/app/item", '--profile-directory="Default"' &
start-process "chrome.exe" "http://localhost:8000/app/warehouse", '--profile-directory="Default"' &
start-process "chrome.exe" "http://localhost:8000/app/item-group", '--profile-directory="Default"' &
start-process "chrome.exe" "http://localhost:8000/app/uom", '--profile-directory="Default"' &
start-process "chrome.exe" "http://localhost:8000/app/stock-entry", '--profile-directory="Default"' &
start-process "chrome.exe" "http://localhost:8000/app/repost-item-valuation", '--profile-directory="Default"' &

# Testing Checkin

start-process "chrome.exe" "http://localhost:8000/app/nr-checkin-import", '--profile-directory="Default"' &
start-process "chrome.exe" "http://localhost:8000/app/employee", '--profile-directory="Default"' &
start-process "chrome.exe" "http://localhost:8000/app/shift-type", '--profile-directory="Default"' &
start-process "chrome.exe" "http://localhost:8000/app/shift-assignment", '--profile-directory="Default"' &
start-process "chrome.exe" "http://localhost:8000/app/employee-checkin", '--profile-directory="Default"' &
start-process "chrome.exe" "http://localhost:8000/app/attendance", '--profile-directory="Default"' &

# Testing Stock Entry
start-process "chrome.exe" "http://localhost:8000/app/nr-stock-entry-import", '--profile-directory="Default"' &
start-process "chrome.exe" "http://localhost:8000/app/item", '--profile-directory="Default"' &
start-process "chrome.exe" "http://localhost:8000/app/stock-entry", '--profile-directory="Default"' &
