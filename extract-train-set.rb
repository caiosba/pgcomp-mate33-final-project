require 'net/http'
require 'nokogiri'
require 'open-uri'

def normalize(text)
  text.to_s.gsub('"', "'").chomp.gsub('É #FAKE que ', '')
end

PARAMS = {
  false: {
    url_base: 'https://g1.globo.com/fato-ou-fake/coronavirus/index/feed/pagina',
    max_page: 20
  },
  verified: {
    url_base: 'https://g1.globo.com/bemestar/coronavirus/index/feed/pagina',
    max_page: 20
  }
}

PARAMS.each do |label, params|
  o = File.open("test-#{label}.txt", 'w+')
  max_page = params[:max_page]
  (1..max_page).to_a.each do |page|
    doc = Nokogiri::HTML(open("#{params[:url_base]}-#{page}.ghtml"))
    doc.css('.bastian-page .bastian-feed-item').each do |item|
      title = normalize(item.at_css('.feed-post-link')&.text)
      o.puts(title.tr("\n", ' ').chomp.strip)
    end
    puts "Parsed page #{page}/#{max_page} for label #{label}..."
  end
  o.close
end
