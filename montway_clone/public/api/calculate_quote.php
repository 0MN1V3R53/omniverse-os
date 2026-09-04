<?php
/**
 * calculate_quote.php — Sky Auto Services Master Pricing Engine v3
 * Omniverse Group | Priya Patel (Technical SEO)
 */
header('Content-Type: application/json; charset=utf-8');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: POST, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type, Accept');
if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') { http_response_code(204); exit; }
if ($_SERVER['REQUEST_METHOD'] !== 'POST') { http_response_code(405); echo json_encode(['success'=>false,'error'=>'Method not allowed']); exit; }
$body = json_decode(file_get_contents('php://input'), true);
if (!$body) { http_response_code(400); echo json_encode(['success'=>false,'error'=>'Invalid JSON']); exit; }

$SP=['AL'=>['r'=>0.92,'t'=>'Standard'],'AK'=>['r'=>1.80,'t'=>'Rural'],'AZ'=>['r'=>0.95,'t'=>'Snowbird'],
'AR'=>['r'=>0.96,'t'=>'Standard'],'CA'=>['r'=>0.90,'t'=>'Hub'],'CO'=>['r'=>1.10,'t'=>'Standard'],
'CT'=>['r'=>0.97,'t'=>'Standard'],'DE'=>['r'=>0.96,'t'=>'Standard'],'FL'=>['r'=>0.85,'t'=>'Snowbird'],
'GA'=>['r'=>0.89,'t'=>'Hub'],'HI'=>['r'=>2.20,'t'=>'Rural'],'ID'=>['r'=>1.25,'t'=>'Rural'],
'IL'=>['r'=>0.92,'t'=>'Hub'],'IN'=>['r'=>0.94,'t'=>'Standard'],'IA'=>['r'=>1.00,'t'=>'Standard'],
'KS'=>['r'=>1.02,'t'=>'Standard'],'KY'=>['r'=>0.95,'t'=>'Standard'],'LA'=>['r'=>0.93,'t'=>'Standard'],
'ME'=>['r'=>1.18,'t'=>'Rural'],'MD'=>['r'=>0.93,'t'=>'Hub'],'MA'=>['r'=>0.96,'t'=>'Hub'],
'MI'=>['r'=>1.00,'t'=>'Standard'],'MN'=>['r'=>1.05,'t'=>'Standard'],'MS'=>['r'=>0.97,'t'=>'Standard'],
'MO'=>['r'=>0.94,'t'=>'Standard'],'MT'=>['r'=>1.50,'t'=>'Rural'],'NE'=>['r'=>1.05,'t'=>'Standard'],
'NV'=>['r'=>0.92,'t'=>'Hub'],'NH'=>['r'=>1.10,'t'=>'Standard'],'NJ'=>['r'=>0.95,'t'=>'Hub'],
'NM'=>['r'=>1.12,'t'=>'Standard'],'NY'=>['r'=>0.95,'t'=>'Hub'],'NC'=>['r'=>0.92,'t'=>'Standard'],
'ND'=>['r'=>1.35,'t'=>'Rural'],'OH'=>['r'=>0.93,'t'=>'Hub'],'OK'=>['r'=>0.98,'t'=>'Standard'],
'OR'=>['r'=>1.08,'t'=>'Standard'],'PA'=>['r'=>0.93,'t'=>'Hub'],'RI'=>['r'=>0.97,'t'=>'Standard'],
'SC'=>['r'=>0.91,'t'=>'Standard'],'SD'=>['r'=>1.30,'t'=>'Rural'],'TN'=>['r'=>0.91,'t'=>'Standard'],
'TX'=>['r'=>0.88,'t'=>'Hub'],'UT'=>['r'=>1.05,'t'=>'Standard'],'VT'=>['r'=>1.20,'t'=>'Rural'],
'VA'=>['r'=>0.92,'t'=>'Standard'],'WA'=>['r'=>1.05,'t'=>'Standard'],'WV'=>['r'=>1.10,'t'=>'Standard'],
'WI'=>['r'=>1.02,'t'=>'Standard'],'WY'=>['r'=>1.45,'t'=>'Rural'],'DC'=>['r'=>0.93,'t'=>'Hub']];

$SA=['Alabama'=>'AL','Alaska'=>'AK','Arizona'=>'AZ','Arkansas'=>'AR','California'=>'CA',
'Colorado'=>'CO','Connecticut'=>'CT','Delaware'=>'DE','Florida'=>'FL','Georgia'=>'GA',
'Hawaii'=>'HI','Idaho'=>'ID','Illinois'=>'IL','Indiana'=>'IN','Iowa'=>'IA','Kansas'=>'KS',
'Kentucky'=>'KY','Louisiana'=>'LA','Maine'=>'ME','Maryland'=>'MD','Massachusetts'=>'MA',
'Michigan'=>'MI','Minnesota'=>'MN','Mississippi'=>'MS','Missouri'=>'MO','Montana'=>'MT',
'Nebraska'=>'NE','Nevada'=>'NV','New Hampshire'=>'NH','New Jersey'=>'NJ','New Mexico'=>'NM',
'New York'=>'NY','North Carolina'=>'NC','North Dakota'=>'ND','Ohio'=>'OH','Oklahoma'=>'OK',
'Oregon'=>'OR','Pennsylvania'=>'PA','Rhode Island'=>'RI','South Carolina'=>'SC','South Dakota'=>'SD',
'Tennessee'=>'TN','Texas'=>'TX','Utah'=>'UT','Vermont'=>'VT','Virginia'=>'VA',
'Washington'=>'WA','West Virginia'=>'WV','Wisconsin'=>'WI','Wyoming'=>'WY','District of Columbia'=>'DC'];

$SC=['AL'=>[32.81,-86.79],'AK'=>[61.37,-152.40],'AZ'=>[34.05,-111.09],'AR'=>[34.80,-92.20],
'CA'=>[36.78,-119.42],'CO'=>[39.55,-105.78],'CT'=>[41.60,-73.09],'DE'=>[38.91,-75.53],
'FL'=>[27.66,-81.52],'GA'=>[33.04,-83.64],'HI'=>[21.09,-157.50],'ID'=>[44.07,-114.74],
'IL'=>[40.63,-89.40],'IN'=>[40.27,-86.13],'IA'=>[41.88,-93.10],'KS'=>[39.01,-98.48],
'KY'=>[37.84,-84.27],'LA'=>[31.24,-92.15],'ME'=>[45.25,-69.45],'MD'=>[39.05,-76.64],
'MA'=>[42.41,-71.38],'MI'=>[44.31,-85.60],'MN'=>[46.73,-94.69],'MS'=>[32.35,-89.40],
'MO'=>[37.96,-91.83],'MT'=>[46.88,-110.36],'NE'=>[41.49,-99.90],'NV'=>[38.80,-116.42],
'NH'=>[43.45,-71.56],'NJ'=>[40.06,-74.41],'NM'=>[34.52,-105.87],'NY'=>[43.30,-74.22],
'NC'=>[35.76,-79.02],'ND'=>[47.55,-101.00],'OH'=>[40.42,-82.91],'OK'=>[35.01,-97.09],
'OR'=>[44.00,-120.50],'PA'=>[41.20,-77.19],'RI'=>[41.58,-71.48],'SC'=>[33.84,-81.16],
'SD'=>[43.97,-99.90],'TN'=>[35.52,-86.58],'TX'=>[31.97,-99.90],'UT'=>[39.32,-111.09],
'VT'=>[44.56,-72.58],'VA'=>[37.43,-78.66],'WA'=>[47.75,-120.74],'WV'=>[38.60,-80.45],
'WI'=>[43.78,-88.79],'WY'=>[43.08,-107.29],'DC'=>[38.91,-77.04]];

$SNOWBIRD=['FL','AZ','NV','TX','SC','GA','AL','LA','MS'];
$WINTER_N=['MT','ND','SD','WY','MN','ME','VT','NH','WI','MI','AK','ID'];
$VF=['sedan'=>0,'suv_small'=>200,'suv_large'=>250,'pickup_half'=>150,'pickup_heavy'=>350,
     'van'=>200,'sports_car'=>350,'classic'=>100,'motorcycle'=>-100,'ev'=>350,'heavy'=>500];
$TM=['open_standard'=>1.00,'enclosed_standard'=>1.40,'enclosed_liftgate'=>1.60,'express_expedited'=>1.90];
$TMN=['open_standard'=>399,'enclosed_standard'=>599,'enclosed_liftgate'=>799,'express_expedited'=>999];
$VL=['sedan'=>'Sedan / Coupe','suv_small'=>'Small SUV / Crossover','suv_large'=>'Large SUV / Full-Size',
     'pickup_half'=>'1/2 Ton Pickup Truck','pickup_heavy'=>'Heavy-Duty Pickup','van'=>'Minivan / Passenger Van',
     'sports_car'=>'Sports Car / Exotic','classic'=>'Classic / Antique','motorcycle'=>'Motorcycle / Powersports',
     'ev'=>'Electric Vehicle (EV)','heavy'=>'Heavy Truck / Commercial'];
$TL=['open_standard'=>'Open Carrier Transport','enclosed_standard'=>'Enclosed',
     'enclosed_liftgate'=>'Enclosed Shielded','express_expedited'=>'Open Express'];

function hav($la1,$lo1,$la2,$lo2){$R=3958.8;$t=M_PI/180;$a=sin(($la2-$la1)*$t/2)**2+cos($la1*$t)*cos($la2*$t)*sin(($lo2-$lo1)*$t/2)**2;return round(2*$R*asin(sqrt($a))*1.18);}
function r5($n){return round($n/5)*5;}
function gAbbr($lbl,$SA,$SP){
  if(!$lbl)return null;
  $v = strtolower(trim($lbl));
  if(preg_match('/^\d{5}/', $v)){
      $z = intval(substr($v,0,5));
      if($z>=90000 && $z<=96199) return 'CA';
      if($z>=32000 && $z<=34999) return 'FL';
      if($z>=82000 && $z<=83199) return 'WY';
      if($z>=80000 && $z<=81699) return 'CO';
      if($z>=59000 && $z<=59999) return 'MT';
      if($z>=10000 && $z<=14999) return 'NY';
      if($z>=75000 && $z<=79999) return 'TX';
      if($z>=60000 && $z<=62999) return 'IL';
      if($z>=30000 && $z<=31999) return 'GA';
      return null;
  }
  $pts=preg_split('/[,\s]+/',trim($lbl));
  foreach(array_reverse($pts)as$p){$c=strtoupper($p);if(isset($SP[$c]))return $c;}
  foreach($SA as$name=>$abbr){if(stripos($lbl,$name)!==false)return $abbr;}
  return null;
}

$orig=trim($body['origin']??''); $dest=trim($body['destination']??'');
$oA=gAbbr($orig,$SA,$SP); $dA=gAbbr($dest,$SA,$SP);
$oD=isset($SP[$oA]) ? $SP[$oA] : ['r'=>1.15,'t'=>'Standard']; 
$dD=isset($SP[$dA]) ? $SP[$dA] : ['r'=>1.15,'t'=>'Standard'];
$miles=intval($body['distance_miles']??0);

$oLat = $body['originGeo']['lat'] ?? null;
$oLon = $body['originGeo']['lon'] ?? null;
$dLat = $body['destGeo']['lat'] ?? null;
$dLon = $body['destGeo']['lon'] ?? null;

if (!$oLat || !$dLat) {
    preg_match('/\b(\d{5})\b/', $orig, $oM);
    preg_match('/\b(\d{5})\b/', $dest, $dM);
    if (!empty($oM[1]) && !empty($dM[1])) {
        $zipDataFile = __DIR__ . '/../assets/data/zip_coordinates.json';
        if (file_exists($zipDataFile)) {
            $zipData = json_decode(file_get_contents($zipDataFile), true);
            if (isset($zipData[$oM[1]]) && isset($zipData[$dM[1]])) {
                $oLat = $zipData[$oM[1]]['lat'];
                $oLon = $zipData[$oM[1]]['lon'];
                $dLat = $zipData[$dM[1]]['lat'];
                $dLon = $zipData[$dM[1]]['lon'];
            }
        }
    }
}

if ($miles <= 0 && $oLat && $dLat) {
    $osrmUrl = "http://router.project-osrm.org/route/v1/driving/{$oLon},{$oLat};{$dLon},{$dLat}?overview=false";
    $ctx = stream_context_create(["http" => ["method" => "GET", "timeout" => 5]]);
    $osrmRes = @file_get_contents($osrmUrl, false, $ctx);
    if ($osrmRes) {
        $osrmData = json_decode($osrmRes, true);
        if (isset($osrmData['routes'][0]['distance'])) {
            $miles = round($osrmData['routes'][0]['distance'] / 1609.34);
        }
    }
    if ($miles <= 0) $miles = hav($oLat, $oLon, $dLat, $dLon);
}

if($miles<=0&&isset($SC[$oA])&&isset($SC[$dA])){$oC=$SC[$oA];$dC=$SC[$dA];$miles=hav($oC[0],$oC[1],$dC[0],$dC[1]);}
if($miles<=0)$miles=1000;
$rate=($oD['r']+$dD['r'])/2.0;
$dm=$miles>2000?0.80:($miles>1000?0.90:($miles>500?1.00:($miles<=199?2.60:1.15)));
$er=$rate*$dm;
if($miles<=199){ $er = max(2.15, min(3.15, $er)); }
$bc=$miles*$er;
$oT=$oD['t']; $dT=$dD['t'];
if(in_array($oT,['Hub','Snowbird'])&&in_array($dT,['Hub','Snowbird']))$bc*=0.90;
elseif($oT==='Rural'&&$dT==='Rural')$bc*=1.25;
$mon=intval(date('n')); $sm=1.00;
if(in_array($mon,[10,11,12])&&in_array($dA,$SNOWBIRD)&&!in_array($oA,$SNOWBIRD))$sm=1.20;
elseif(in_array($mon,[4,5])&&in_array($oA,$SNOWBIRD)&&!in_array($dA,$SNOWBIRD))$sm=1.18;
elseif(in_array($mon,[12,1,2])&&(in_array($oA,$WINTER_N)||in_array($dA,$WINTER_N)))$sm=1.10;
$bc*=$sm;
$vt=$body['vehicleType']??'sedan'; $vs=$VF[$vt]??0; $bc+=$vs;
$is=0; if(($body['vehicleCondition']??'')==='inoperable'){$is=150;$bc+=150;}
$tt=$body['transportType']??'open_standard'; $tmult=$TM[$tt]??1.00; $tmin=$TMN[$tt]??399;
$cost=$bc*$tmult; $tsc=$cost-$bc;
$vv=$body['vehicleValue']??'under_50k'; $vvs=0;
if($vv==='50k_100k'){$vvs=$cost*0.15;$cost*=1.15;}
elseif($vv==='over_100k'){$vvs=$cost*0.30;$cost*=1.30;}
$cost=max($cost,$tmin,399);
$mid=max(399, r5($cost)); $lo=max(399, r5($cost*0.90)); $hi=max(399, r5($cost*1.10));
$etad=max(1,(int)ceil($miles/450)); $eta=$etad===1?'1 day':"$etad days";
$rt=($oT==='Rural'&&$dT==='Rural')?'Rural-Rural (+25%)':(in_array($oT,['Hub','Snowbird'])&&in_array($dT,['Hub','Snowbird'])?'Hub-Hub (-10%)':'Standard');

echo json_encode(['success'=>true,'data'=>[
    'miles'=>$miles,'mid'=>$mid,'lo'=>$lo,'hi'=>$hi,'eta'=>$eta,
    'originAbbr'=>$oA,'destAbbr'=>$dA,'vehicleLabel'=>$VL[$vt]??$vt,
    'transportLabel'=>$TL[$tt]??$tt,'originLabel'=>$orig,'destLabel'=>$dest,
    'originGeo'=>($oLat && $oLon) ? ['lat'=>$oLat,'lon'=>$oLon] : null,
    'destGeo'=>($dLat && $dLon) ? ['lat'=>$dLat,'lon'=>$dLon] : null,
    'breakdown'=>['baseRate'=>round($er,3),'baseMilesCost'=>round($miles*$er),'seasonalMult'=>$sm,
        'baseRatePerMile'=>round($er,3),'baseCost'=>round($miles*$er),
        'routeType'=>$rt,'vehicleSurcharge'=>$vs,'inoperableSurcharge'=>$is,
        'transportSurcharge'=>round($tsc),'valueSurcharge'=>round($vvs)]]]);
