$network = "192.168.1"  # Adjust this to your network range
$jobs = @()

for ($i = 1; $i -le 254; $i++) {
    $ip = "$network.$i"
    $jobs += Start-Job -ScriptBlock {
        param($ip)
        $pingResult = Test-Connection -ComputerName $ip -Count 1 -Quiet
        if ($pingResult) {
            "$ip is alive"
        }
    } -ArgumentList $ip
}

$jobs | Wait-Job | Receive-Job
