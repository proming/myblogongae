function Jumping(){
  var jumpPage = document.pageForm.jumpPage.value;
  if(isNaN(jumpPage)) {
    document.pageForm.jumpPage.value = 1;
    jumpPage = 1;
  }
  if(parseInt(jumpPage) >= max_page) {
	  document.pageForm.jumpPage.value = max_page;
  }
  document.pageForm.submit();
  return ;
}
function gotoPage(pagenum){
  document.pageForm.jumpPage.value = pagenum;
  document.pageForm.submit();
  return ;
}
