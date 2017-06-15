<!DOCTYPE html>
	<head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
    <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1.0, user-scalable=no"/>
    <title> 8-Ball Rankings </title>

    <link href="css/materialize.css" type="text/css" rel="stylesheet" media="screen,projection"/>
	  <link href="css/style.css" type="text/css" rel="stylesheet" media="screen,projection"/>
	<link rel="shortcut icon" type="image/x-icon" href="favicon.ico" />

	  	
  	<style>
      #badplayerexpand {
        width:100%;
        display:none;
      }
    </style>
	</head>
	<body>
    <nav class="black">
      <div class="navbar-wrapper container">
        <center><div class="brand-logo" style="color:white;position:relative" > 8-Ball</div></center>
      </div>
    </nav>
    <h2 class="header center black-text text-lighten-2">Current Rankings</h2>
      <div class="row center" style="width:70%">
	<table class="highlight responsive-table">
	  <thead>
	    <tr>
	      <th data-field="img" width="15%">Picture</th>
	      <th data-field="name" width="65%">Name</th>
	      <th data-field="elo">Elo</th>
	    <tr>
	  </thead>
	  <tbody>
	    <?php
		$handle = fopen("8ball.dat","r");
		while(($line=fgets($handle)) !== false) {
			if(strlen($line) > 1) {
				$dataarr = explode(",",$line);
				echo "<tr>";
				echo "<td><img width=100 src='" . $dataarr[1] . "'/></td>";
				echo "<td>" . $dataarr[0] . "</td>";
				echo "<td>" . $dataarr[2] . "</td>";
				echo "</tr>";
			}
		}
		fclose($handle);

	    ?>
	  </tbody>
	</table>
      </div>


      	<!-- Materialize -->
      	<script src="js/jquery.js"></script>	
  		<script src="js/materialize.js"></script>
  		<script src="js/init.js"></script>
        <!-- Plugin JavaScript -->
        <script src="js/jquery.easing.min.js"></script>
        <script src="js/jquery.fittext.js"></script>
        <script src="js/wow.min.js"></script>
        <!-- Custom Theme JavaScript -->
        <script src="js/creative.js"></script>
	</body>  
</html>
  
