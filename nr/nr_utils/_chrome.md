# Testing sales process

start-process "chrome.exe" "http://localhost:8000/app/sales-order", '--profile-directory="Default"' &
start-process "chrome.exe" "http://localhost:8000/app/sales-invoice", '--profile-directory="Default"' &
start-process "chrome.exe" "http://localhost:8000/app/payment-entry", '--profile-directory="Default"' &
start-process "chrome.exe" "http://localhost:8000/app/delivery-note", '--profile-directory="Default"' &
start-process "chrome.exe" "http://localhost:8000/app/item", '--profile-directory="Default"' &
start-process "chrome.exe" "http://localhost:8000/app/repost-item-valuation", '--profile-directory="Default"' &
start-process "chrome.exe" "http://localhost:8000/app/customer", '--profile-directory="Default"' &
start-process "chrome.exe" "http://localhost:8000/app/account/view/tree", '--profile-directory="Default"'
