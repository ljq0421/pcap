#include <stdio.h>
#include <string.h>

int main()
{
    char token[] ="abdzxbcdefgh";
    printf("%s\n",token);
    char *tokenremain = token;
    char *tok1 = strsep(&tokenremain,"cde");
    printf("tok1:%s,token:%s\n",tok1,tokenremain);
    tok1 = strsep(&tokenremain,"cde");                                                                  
    printf("tok1:%s,token:%s\n",tok1,tokenremain);
    return 0;
}
