<?php

// Define the PubMed API endpoint
$pubmed_url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi';

// Set the search parameters
$search_term = 'neuroscience';
$search_database = 'pubmed';
$search_retmax = 5;

// Build the query string
$query_string = http_build_query([
    'db' => $search_database,
    'term' => $search_term,
    'retmax' => $search_retmax,
]);

// Send the request to PubMed API
$curl = curl_init();
curl_setopt($curl, CURLOPT_URL, "{$pubmed_url}?{$query_string}");
curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);
$response = curl_exec($curl);
curl_close($curl);

// Parse the response XML
$xml = simplexml_load_string($response);
$id_list = (array) $xml->IdList->Id;

// Define the PubMed API endpoint for retrieving paper details
$pubmed_fetch_url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi';

// Generate HTML code for the papers
$html = '<ul>';
foreach ($id_list as $id) {
    // Build the query string
    $query_string = http_build_query([
        'db' => $search_database,
        'id' => $id,
        'retmode' => 'xml',
    ]);

    // Send the request to PubMed API
    $curl = curl_init();
    curl_setopt($curl, CURLOPT_URL, "{$pubmed_fetch_url}?{$query_string}");
    curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);
    $response = curl_exec($curl);
    curl_close($curl);

    // Parse the response XML
    $xml = simplexml_load_string($response);

    // Extract the paper details
    $title = (string) $xml->PubmedArticle->MedlineCitation->Article->ArticleTitle;
    $authors = array_map(function($author) {
        return (string) $author->LastName . ' ' . (string) $author->Initials;
    }, (array) $xml->PubmedArticle->MedlineCitation->Article->AuthorList->Author);
    $journal = (string) $xml->PubmedArticle->MedlineCitation->Article->Journal->Title;
    $doi = (string) $xml->PubmedArticle->PubmedData->ArticleIdList->ArticleId[1];

    // Generate the HTML code for the paper
    $html .= "<li><strong>{$title}</strong><br>";
    $html .= implode(', ', $authors) . "<br>";
    $html .= "{$journal} {$doi}</li>";
}
$html .= '</ul>';

// Print the HTML code
echo $html;
