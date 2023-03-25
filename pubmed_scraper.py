<?php

// Define the PubMed API endpoint
$pubmed_url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi';

// Set the search parameters
$search_term = 'neuroscience';
$search_database = 'pubmed';
$search_retmax = 1;

// Calculate the publication date range for the last week
$start_date = date('Y/m/d', strtotime('-1 week'));
$end_date = date('Y/m/d');

// Build the query string
$query_string = http_build_query([
    'db' => $search_database,
    'term' => $search_term,
    'datetype' => 'pdat',
    'mindate' => $start_date,
    'maxdate' => $end_date,
    'retmax' => $search_retmax,
    'sort' => 'pubdate',
]);

// Send the request to PubMed API

$curl = curl_init();
curl_setopt($curl, CURLOPT_HTTPHEADER, ['Accept: application/xml']);
curl_setopt($curl, CURLOPT_URL, "{$pubmed_url}?{$query_string}");
curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);
$response = curl_exec($curl);
curl_close($curl);

// Parse the response XML
$xml = simplexml_load_string($response);

if (isset($xml->DocSum)) {
    // Extract the paper details
    $docsum = $xml->DocSum;
    $title = (string) $docsum->Item[0]->Title;
    $authors = (string) $docsum->Item[0]->AuthorList->Author[0]->Name;
    $journal = (string) $docsum->Item[0]->FullJournalName;
    $citations = (int) $docsum->Item[0]->LstNIHGrantCount->GrantCount;

    // Get the abstract text from the Pubmed API
    $id = (string) $docsum->Id;
    $abstract_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id={$id}&retmode=xml";
    $abstract_response = curl_exec(curl_init($abstract_url));
    $abstract_xml = simplexml_load_string($abstract_response);
    $abstract = (string) $abstract_xml->PubmedArticle->MedlineCitation->Article->Abstract->AbstractText;

    // Generate the HTML code for the paper
    $html = "<html><head><title>{$title}</title></head><body>";
    $html .= "<ul><li><strong>{$title}</strong><br>";
    $html .= "{$authors}<br>";
    $html .= "{$journal} ({$citations} citations)<br>";
    $html .= "{$abstract}</li></ul>";
    $html .= "</body></html>";

    // Write the HTML code to a file
    $filename = "neuroscience.html";
    $file = fopen($filename, 'w');
    fwrite($file, $html);
    fclose($file);

    echo "Static HTML page generated: {$filename}";
} else {
    echo "No results found.";
}

?>
