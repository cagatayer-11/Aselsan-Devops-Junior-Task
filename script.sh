output="./logs/"
output_file="${output}/$(date)_Current_Load Average"
echo "load average on $(date)" > "$output_file"
uptime >> "$output_file"
