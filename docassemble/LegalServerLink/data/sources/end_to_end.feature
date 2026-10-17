Feature: Complete LegalServerLink interview

  # Reviewed against the interview and its local includes.
  # Static ALDashboard draft curated to the chosen branch; browser validation runs in CI.
  Scenario: Complete LegalServerLink and verify the result
    Given I sign in with the email "ALKILN_ADMIN_EMAIL" and the password "ALKILN_ADMIN_PASSWORD"
    And I start the interview at "sample_letter.yml"
    And the maximum seconds for each Step is 300
    And the user gets to "final_letter" with this data:
      | var | value |
      | legalserver_site_abbreviation | alkiln |
      | legalserver_site_type | Demo |
      | legalserver_matter_uuid | 00000000-0000-4000-8000-000000000001 |
      | legalserver_current_user_uuid | 00000000-0000-4000-8000-000000000002 |
      | client_message.planned_recipient | client |
      | client_message.sender | current_user |
      | client_message.method | Letter |
      | client_message.textoption | CustomLetter |
      | client_message.text | This is a synthetic ALKiln letter for a disposable LegalServer test case. |
      | client_message.letterhead | SampleLetterhead1.docx |
    Then I should see the phrase "Generated Letter"
