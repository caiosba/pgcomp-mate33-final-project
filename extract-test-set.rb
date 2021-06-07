# Get fact-checked content from a certain workspace
# This script must be executed inside Check

WORKSPACE = 'estadao'
LIMIT = 200

['verified', 'false'].each do |label|
  output = File.open("/tmp/train-#{label}.txt", 'w+')
  i = 0
  DynamicAnnotation::Field.where(field_name: 'verification_status_status', value: label).joins(:annotation).joins('INNER JOIN project_medias pm ON pm.id = annotations.annotated_id').where('pm.team_id' => Team.find_by_slug(WORKSPACE).id).select('pm.id').each do |row|
    pm = ProjectMedia.find(row.id)
    next unless ['Claim', 'Link'].include?(pm.media.type)
    if !pm.title.blank? && i < LIMIT
      output.puts(pm.title.tr("\n", ' ').chomp.strip)
      i += 1
    end
  end
  output.close
end
