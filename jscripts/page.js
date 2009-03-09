function Jumping(){
	document.pageForm.jumpPage.value = document.pageForm.jump.value;
  document.pageForm.submit();
  return ;
}
function gotoPage(pagenum){
  document.pageForm.jumpPage.value = pagenum;
  document.pageForm.submit();
  return ;
}
