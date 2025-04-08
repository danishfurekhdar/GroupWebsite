module Jekyll
  class MemberPagesGenerator < Generator
    safe true
    priority :normal

    def generate(site)
      @site = site
      
      # Generate pages for all member types
      generate_member_pages('team_members')
      generate_member_pages('alumni_members') if site.data['alumni_members']
    end

    private

    def generate_member_pages(collection_name)
      return unless @site.data[collection_name]

      @site.data[collection_name].each do |member|
        next unless member['slug'] && !member['slug'].empty?

        # Create the member page
        @site.pages << MemberPage.new(@site, @site.source, member)
      end
    end
  end

  class MemberPage < Page
    def initialize(site, base, member)
      @site = site
      @base = base
      @dir  = member['slug'] # This determines the URL path (/danish/)
      @name = 'index.html'   # Required for proper static site generation

      self.process(@name)
      
      # Load the member layout template
      self.read_yaml(File.join(base, '_layouts'), 'member.html')
      
      # Set the permalink to ensure clean URLs
      self.data['permalink'] = "/#{member['slug']}/"

      # Transfer all member data to page front matter
      member.each do |key, value|
        self.data[key] = value unless value.nil? || value.to_s.empty?
      end

      # Set required page metadata
      self.data['title'] = member['name']
      self.data['layout'] = 'member'
      
      # Set the page content from bio if available
      self.content = member['bio'] || ''
    end
  end
end