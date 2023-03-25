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
curl_setopt($curl, CURLOPT_URL, "{$pubmed_url}?{$query_string}");
curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);
$response = curl_exec($curl);
curl_close($curl);

// Parse the response XML
$xml = simplexml_load_string($response);
$docsum = $xml->DocSum;

// Extract the paper details
$title = (string) $docsum->Item[1]->value;
$authors = (string) $docsum->Item[2]->value;
$journal = (string) $docsum->Item[3]->value;
$citations = (int) $docsum->Item[4]->value;

// Generate the HTML code for the paper
$html = "<ul><li><strong>{$title}</strong><br>";
$html .= "{$authors}<br>";
$html .= "{$journal} ({$citations} citations)</li></ul>";

// Print the HTML code
echo $html;
