<?php

$config = parse_ini_file("google-places.ini");
define ('API_KEY', $config['key']);
define ('SEARCH_API', $config['search_api']);
define ('DETAILS_API', $config['details_api']);

function http_get($url, $params) {
    $params["key"] = API_KEY; 
    $ch = curl_init($url . '?' . http_build_query($params)); 
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    //var_dump(curl_getinfo($ch));
    $result = curl_exec($ch);
    curl_close($ch);
    return $result;
}

function get_place($query) {
    $result_json = json_decode( http_get(SEARCH_API, array("query" => $query) ));
    $place = $result_json->results[0];
    
    return array("name" => $place->name, "id" => $place->place_id, "address" => $place->formatted_address);
}

function get_details($placeid) {
    $result = http_get( DETAILS_API, array('placeid' => $placeid));
    $result_json = json_decode( http_get(DETAILS_API, array("placeid" => $placeid)));
    $result = $result_json->result;
    if (!isset($result->rating) || !$result->rating) {
        return null;
    } else {
        $rating = $result->rating;
        $reviews_all = $result->reviews;
        $reviews = array(); //tdClass();
        foreach ($reviews_all as $i => $review) {
            $reviews[$i] = new stdClass();
            $reviews[$i]->author = array($review->author_name);
            $reviews[$i]->rating = array($review->rating);
            $reviews[$i]->text = array($review->text);
        }
        return array('rating' => $rating, 'reviews' => $reviews);
    }
}

if (php_sapi_name() == 'cli') {
    if ($argc < 2) die("Missing query");
    $query = "{$argv[1]} near {$argv[2]}";
} else {
    if (!isset($_GET['q'])) die("Missing query");
    $query = urlencode("{$_GET['q']} near {$_GET['place']}");
}

$place = get_place($query);
$rnr = get_details($place['id']);
if ($rnr == null) {
	$rnr = array();
}
echo json_encode($place + $rnr);


?>
